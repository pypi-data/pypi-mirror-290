import time
import requests
import logging
import re
from requests.exceptions import RequestException
from urllib.parse import urlparse


class CymulateOAuth2Client:
    ISSUER = 'cymulate.com'
    AUDIENCE = 'cymulate.com'

    def __init__(self, client_id, client_secret, base_url, scope=None, max_retries=3, retry_delay=2):
        self._validate_client_id(client_id)
        self._validate_base_url(base_url)

        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url.rstrip('/')
        self.scope = scope
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.token_url = f"{self.base_url}/token"
        self.revoke_url = f"{self.base_url}/revoke"

        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = 0

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_client_id(self, client_id):
        """Validate that the client_id is a valid MongoDB ObjectId using a regex."""
        if not re.fullmatch(r"^[a-fA-F0-9]{24}$", client_id):
            raise ValueError(
                f"Invalid client_id: {client_id}. Must be a valid 24-character hexadecimal MongoDB ObjectId.")

    def _validate_base_url(self, base_url):
        """Validate that the base_url is a well-formed URL."""
        parsed_url = urlparse(base_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid base_url: {base_url}. Must be a valid URL.")

    def _make_request(self, url, data, headers=None):
        """Utility method to make a POST request."""
        headers = headers or {}
        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, data=data, headers=headers)
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

    def _get_new_tokens(self):
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

    def _refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            self.logger.info("No refresh token available. Obtaining new tokens.")
            self._get_new_tokens()
            return

        self.logger.info("Refreshing access token...")
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        response_data = self._make_request(self.token_url, data)
        self._set_tokens(response_data)

    def _set_tokens(self, response_data):
        """Set the access and refresh tokens from the response."""
        self.access_token = response_data.get('access_token')
        self.refresh_token = response_data.get('refresh_token')
        self.token_expires_at = time.time() + response_data.get('expires_in', 3600)
        self.logger.info("Access token obtained and set successfully.")

    def _ensure_valid_token(self):
        """Ensure the access token is valid, refreshing or obtaining new tokens if necessary."""
        if self.access_token is None or time.time() >= self.token_expires_at:
            if self.refresh_token:
                self._refresh_access_token()
            else:
                self._get_new_tokens()

    def _prepare_headers(self, headers):
        """Prepare headers with Authorization token."""
        headers = headers or {}
        headers['Authorization'] = f'Bearer {self.access_token}'
        return headers

    def request(self, method, url, **kwargs):
        """Make an authenticated request to a secure resource."""
        self._ensure_valid_token()
        headers = self._prepare_headers(kwargs.pop('headers', {}))

        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, headers=headers, **kwargs)
                if response.status_code == 401:
                    self.logger.info("Unauthorized. Refreshing token and retrying request.")
                    self._refresh_access_token()
                    headers['Authorization'] = f'Bearer {self.access_token}'
                    response = requests.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

    def get(self, url, **kwargs):
        """GET request to a secure resource."""
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """POST request to a secure resource."""
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """PUT request to a secure resource."""
        return self.request('PUT', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        """DELETE request to a secure resource."""
        return self.request('DELETE', url, **kwargs)

    def revoke_token(self, token=None, token_type_hint='access_token'):
        """Revoke a token on the server."""
        if not token:
            token = self.refresh_token if token_type_hint == 'refresh_token' else self.access_token
            if not token:
                raise Exception(f"No {token_type_hint} available to revoke.")

        self.logger.info(f"Revoking {token_type_hint}...")
        data = {
            'token': token,
            'token_type_hint': token_type_hint
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response_data = self._make_request(self.revoke_url, data, headers)
        self._clear_tokens(token)

    def _clear_tokens(self, token):
        """Clear the access or refresh token if revoked."""
        if token == self.access_token or token == self.refresh_token:
            self.access_token = None
            self.refresh_token = None
            self.token_expires_at = 0
        self.logger.info("Token revoked and cleared successfully.")
