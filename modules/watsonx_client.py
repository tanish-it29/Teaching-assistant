"""
watsonx_client.py — IBM watsonx.ai API client.

This is the ONLY module that imports from ibm-watsonx-ai.
All other modules interact with the AI through this class.

Usage:
    client = WatsonXClient(api_key="...", project_id="...", url="...")
    client.connect()
    text = client.generate("Your prompt here", max_tokens=800)

Credentials should be loaded from environment variables or the Streamlit
sidebar — never hardcoded in source code.
"""

import os
from modules.config import MODEL_ID, DEFAULT_WATSONX_URL


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class WatsonXConnectionError(Exception):
    """Raised when the client cannot connect to IBM watsonx.ai (bad credentials or network)."""


class WatsonXTimeoutError(Exception):
    """Raised when the IBM watsonx.ai API takes too long to respond."""


class WatsonXEmptyResponseError(Exception):
    """Raised when the model returns an empty or unusable response."""


class WatsonXAPIError(Exception):
    """Raised for unexpected API errors not covered by the above exceptions."""


# ---------------------------------------------------------------------------
# WatsonXClient
# ---------------------------------------------------------------------------

class WatsonXClient:
    """
    Thin wrapper around the ibm-watsonx-ai SDK.

    Attributes:
        api_key    -- IBM Cloud API key
        project_id -- watsonx.ai project ID
        url        -- Regional endpoint URL
        _model     -- ModelInference instance (created on connect())
    """

    def __init__(self, api_key: str, project_id: str, url: str = DEFAULT_WATSONX_URL) -> None:
        self.api_key: str = api_key
        self.project_id: str = project_id
        self.url: str = url
        self._model = None  # Set by connect()

    def connect(self) -> None:
        """
        Initialise the connection to IBM watsonx.ai.

        Raises:
            WatsonXConnectionError: if credentials are invalid or the network is unreachable.
        """
        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference

            credentials = Credentials(url=self.url, api_key=self.api_key)
            self._model = ModelInference(
                model_id=MODEL_ID,
                credentials=credentials,
                project_id=self.project_id,
            )
        except ImportError as exc:
            raise WatsonXConnectionError(
                "ibm-watsonx-ai package is not installed. "
                "Run: pip install ibm-watsonx-ai"
            ) from exc
        except Exception as exc:
            raise WatsonXConnectionError(
                f"Could not connect to IBM watsonx.ai: {exc}"
            ) from exc

    def generate(self, prompt: str, max_tokens: int = 800) -> str:
        """
        Send a prompt to the Granite model and return the generated text.

        Args:
            prompt:     The full prompt string.
            max_tokens: Maximum number of new tokens to generate.

        Returns:
            The generated text as a string.

        Raises:
            WatsonXConnectionError:   if generate() is called before connect().
            WatsonXTimeoutError:      if the API request times out.
            WatsonXEmptyResponseError: if the model returns no usable text.
            WatsonXAPIError:          for any other unexpected API error.
        """
        if self._model is None:
            raise WatsonXConnectionError(
                "Not connected. Call connect() before generate()."
            )

        try:
            response = self._model.generate_text(
                prompt=prompt,
                params={"max_new_tokens": max_tokens},
                guardrails=True,
            )
        except TimeoutError as exc:
            raise WatsonXTimeoutError(
                "The request to IBM watsonx.ai timed out. Please try again."
            ) from exc
        except Exception as exc:
            error_msg = str(exc).lower()
            if "timeout" in error_msg or "timed out" in error_msg:
                raise WatsonXTimeoutError(
                    "The request to IBM watsonx.ai timed out. Please try again."
                ) from exc
            if "unauthorized" in error_msg or "401" in error_msg or "403" in error_msg:
                raise WatsonXConnectionError(
                    "Authentication failed. Check your IBM watsonx API Key and Project ID."
                ) from exc
            raise WatsonXAPIError(
                f"IBM watsonx.ai returned an unexpected error: {exc}"
            ) from exc

        # Validate the response
        if not response or not str(response).strip():
            raise WatsonXEmptyResponseError(
                "The model returned an empty response. Try rephrasing your input."
            )

        return str(response).strip()

    @property
    def is_connected(self) -> bool:
        """True if connect() has been called successfully."""
        return self._model is not None


# ---------------------------------------------------------------------------
# Helper: load credentials from environment variables
# ---------------------------------------------------------------------------

def load_credentials_from_env() -> dict[str, str]:
    """
    Read watsonx credentials from environment variables.
    Returns a dict with keys 'api_key', 'project_id', 'url'.
    Values will be empty strings if the variables are not set.

    Environment variables:
        WATSONX_API_KEY
        WATSONX_PROJECT_ID
        WATSONX_URL  (optional, defaults to us-south endpoint)
    """
    return {
        "api_key": os.environ.get("WATSONX_API_KEY", ""),
        "project_id": os.environ.get("WATSONX_PROJECT_ID", ""),
        "url": os.environ.get("WATSONX_URL", DEFAULT_WATSONX_URL),
    }
