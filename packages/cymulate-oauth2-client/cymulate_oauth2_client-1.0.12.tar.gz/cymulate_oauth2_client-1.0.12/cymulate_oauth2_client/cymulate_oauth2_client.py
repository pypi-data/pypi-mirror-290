import time
import requests
import logging
import re
import atexit
import threading
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
from urllib.parse import urlparse
from typing import Optional, Dict, Any, final, Self, Union
from tenacity import retry, stop_after_attempt, wait_fixed

JsonResponse = Dict[str, Any]
Headers = Optional[Dict[str, str]]


@final
class CymulateOAuth2Client:
    ISSUER: str = 'cymulate.com'
    AUDIENCE: str = 'cymulate.com'

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            base_url: str,
            scope: Optional[str] = None,
            max_retries: int = 3,
            retry_delay: int = 2
    ) -> None:
        self._validate_client_id(client_id)
        self._validate_base_url(base_url)

        self.token_lock = threading.Lock()
        self._initialize_credentials(client_id, client_secret, base_url, scope)
        self._initialize_retry_settings(max_retries, retry_delay)
        self._initialize_token_urls(base_url)
        self._initialize_tokens()
        self._setup_logging()
        self._register_exit_handler()

    def _initialize_credentials(self, client_id: str, client_secret: str, base_url: str, scope: Optional[str]) -> None:
        """Initialize client credentials and related parameters."""
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.base_url: str = base_url.rstrip('/')
        self.scope: Optional[str] = scope

    def _initialize_retry_settings(self, max_retries: int, retry_delay: int) -> None:
        """Initialize retry settings."""
        self.max_retries: int = max_retries
        self.retry_delay: int = retry_delay

    def _initialize_token_urls(self, base_url: str) -> None:
        """Initialize token and revoke URLs."""
        self.token_url: str = f"{self.base_url}/oauth2/token"
        self.revoke_url: str = f"{self.base_url}/oauth2/revoke"

    def _initialize_tokens(self) -> None:
        """Initialize token-related variables."""
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: float = 0.0
        self.tokens_revoked: bool = False

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _register_exit_handler(self) -> None:
        """Register the token revocation handler to be called on exit."""
        atexit.register(self._revoke_tokens_on_exit)

    @staticmethod
    def _validate_client_id(client_id: str) -> None:
        """Validate that the client_id is a valid MongoDB ObjectId using a regex."""
        if not re.fullmatch(r"^[a-fA-F0-9]{24}$", client_id):
            raise ValueError(
                f"Invalid client_id: {client_id}. Must be a valid 24-character hexadecimal MongoDB ObjectId."
            )

    @staticmethod
    def _validate_base_url(base_url: str) -> None:
        """Validate that the base_url is a well-formed URL."""
        parsed_url = urlparse(base_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid base_url: {base_url}. Must be a valid URL.")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _make_request(self, url: str, data: JsonResponse, headers: Headers = None) -> JsonResponse:
        """Utility method to make a POST request with retries."""
        headers = headers or {}
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def _perform_request(self, method: str, url: str, headers: Headers, **kwargs: Any) -> requests.Response:
        """Internal method to perform an HTTP request and handle retries."""
        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response
            except (HTTPError, ConnectionError, Timeout) as e:
                self.logger.warning(f"{type(e).__name__} on attempt {attempt + 1}: {str(e)}")
                if isinstance(e, HTTPError) and response.status_code == 401:
                    raise
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

    def _get_new_tokens(self) -> None:
        """Obtain new tokens from the OAuth2 server."""
        self.logger.info("Obtaining new access token...")
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': self.AUDIENCE,
            'issuer': self.ISSUER,
        }
        if self.scope:
            data['scope'] = self.scope

        response_data = self._make_request(self.token_url, data)
        self._set_tokens(response_data)

    def _refresh_access_token(self) -> Self:
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            self.logger.info("No refresh token available. Obtaining new tokens.")
            self._get_new_tokens()
            return self

        self.logger.info("Refreshing access token...")
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        try:
            response_data = self._make_request(self.token_url, data)
            self._set_tokens(response_data)
        except RequestException:
            self.logger.warning("Failed to refresh token, obtaining new tokens.")
            self._get_new_tokens()

        return self

    @final
    def _set_tokens(self, response_data: Dict[str, Any]) -> None:
        """Set the access and refresh tokens from the response."""
        self.access_token = response_data.get('access_token')
        self.refresh_token = response_data.get('refresh_token')
        self.token_expires_at = time.time() + response_data.get('expires_in', 3600)
        self.logger.info("Access token set successfully. Token expires at {}".format(time.ctime(self.token_expires_at)))

    def _ensure_valid_token(self) -> None:
        """Ensure the access token is valid, refreshing or obtaining new tokens if necessary."""
        with self.token_lock:
            if self.access_token is None or time.time() >= self.token_expires_at - 30:
                if self.refresh_token:
                    self._refresh_access_token()
                else:
                    self._get_new_tokens()

    def _prepare_headers(self, headers: Headers) -> Dict[str, str]:
        """Prepare headers with Authorization token."""
        headers = headers or {}
        headers['Authorization'] = f'Bearer {self.access_token}'
        return headers

    def request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        """Make an authenticated request to a secure resource."""
        self._ensure_valid_token()
        headers = self._prepare_headers(kwargs.pop('headers', {}))
        response = self._perform_request(method, url, headers, **kwargs)
        if response.status_code == 401:
            self.logger.info("Unauthorized. Refreshing token and retrying request.")
            self._refresh_access_token()
            headers['Authorization'] = f'Bearer {self.access_token}'
            response = self._perform_request(method, url, headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """GET request to a secure resource."""
        return self.request('GET', f"{self.base_url}{path}", **kwargs)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None,
             **kwargs: Any) -> Dict[str, Any]:
        """POST request to a secure resource."""
        return self.request('POST', f"{self.base_url}{path}", data=data, json=json, **kwargs)

    def put(self, path: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        """PUT request to a secure resource."""
        return self.request('PUT', f"{self.base_url}{path}", data=data, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """DELETE request to a secure resource."""
        return self.request('DELETE', f"{self.base_url}{path}", **kwargs)

    def revoke_token(self, token: Optional[str] = None, token_type_hint: str = 'access_token') -> None:
        """Revoke a token on the server."""
        if self.tokens_revoked:
            self.logger.info("Tokens already revoked, skipping further revocation.")
            return

        if not token:
            token = self.refresh_token if token_type_hint == 'refresh_token' else self.access_token
            if not token:
                self.logger.error(f"No {token_type_hint} available to revoke.")
                return

        self.logger.info(f"Revoking {token_type_hint}...")
        data = {
            'token': token,
            'token_type_hint': token_type_hint
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response_data = self._make_request(self.revoke_url, data, headers)
            if 'message' in response_data and response_data['message'] == 'Token revoked successfully':
                self._clear_tokens(token, token_type_hint)
                self.tokens_revoked = True
            else:
                self.logger.error("Failed to revoke token.")
        except Exception as e:
            self.logger.error(f"Failed to revoke {token_type_hint}: {str(e)}")

    def _clear_tokens(self, token: str, token_type_hint: str) -> None:
        """Clear the access or refresh token if revoked."""
        if token_type_hint == 'access_token':
            self.access_token = None
        elif token_type_hint == 'refresh_token':
            self.refresh_token = None
        self.token_expires_at = 0
        self.logger.info(f"{token_type_hint.capitalize()} revoked and cleared successfully.")

    def _revoke_tokens_on_exit(self) -> None:
        """Revoke tokens when the program exits."""
        if not self.tokens_revoked:
            if self.refresh_token:
                self.logger.info("Revoking refresh_token on script exit...")
                try:
                    self.revoke_token(self.refresh_token, 'refresh_token')
                except Exception as e:
                    self.logger.error(f"Failed to revoke refresh_token: {str(e)}")
                    return

            if self.access_token and not self.tokens_revoked:
                self.logger.info("Revoking access_token on script exit...")
                try:
                    self.revoke_token(self.access_token, 'access_token')
                except Exception as e:
                    self.logger.error(f"Failed to revoke access_token: {str(e)}")
