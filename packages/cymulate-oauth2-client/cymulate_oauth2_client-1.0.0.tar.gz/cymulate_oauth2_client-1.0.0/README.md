# Cymulate OAuth2 Client

A Python client for OAuth2 authentication with Cymulate API. This library helps you to authenticate and interact with the Cymulate API using OAuth2, handling token management and secure requests.

## Installation

To install the package, use pip:

```bash
pip install cymulate-client
```

## Usage

Below is an example of how to use the `CymulateOAuth2Client` class to authenticate with the Cymulate API, make a secure request, and revoke a token.

```python
from cymulate import CymulateOAuth2Client

if __name__ == "__main__":
    CLIENT_ID = '65eedae925808aeda2a61c00'
    CLIENT_SECRET = 'Rl18Q~dJRFoEkhiwJh5X4OtNdWqmrnzotokQWaYV'
    BASE_URL = 'http://api.cymulate.com/oauth2' 

    try:
        client = CymulateOAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            base_url=BASE_URL
        )

        # Accessing a secure resource
        SECURE_URL = "https://api.cymulate.com/v1/browsing/status"

        try:
            response = client.get(SECURE_URL)
            print(f"Response from {SECURE_URL}: {response}")
        except Exception as e:
            print(f"Error accessing {SECURE_URL}: {str(e)}")

        # Revoking the refresh token
        try:
            client.revoke_token(token_type_hint='refresh_token')
        except Exception as e:
            print(f"Error revoking token: {str(e)}")
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
```

### Key Methods

- `get(url, **kwargs)`: Make a GET request to a secure resource.
- `post(url, data=None, json=None, **kwargs)`: Make a POST request to a secure resource.
- `put(url, data=None, **kwargs)`: Make a PUT request to a secure resource.
- `delete(url, **kwargs)`: Make a DELETE request to a secure resource.
- `revoke_token(token=None, token_type_hint='access_token')`: Revoke an OAuth2 token on the server.

### Exception Handling

The client handles common request exceptions and retries the request up to a specified maximum number of retries. If the token is expired or invalid, it automatically refreshes or obtains a new token.

### Logging

The client uses Python’s built-in logging module to log important information, warnings, and errors.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements or bug fixes.

## Contact

For any inquiries or support, please contact Cymulate support at [support@cymulate.com](mailto:support@cymulate.com).
