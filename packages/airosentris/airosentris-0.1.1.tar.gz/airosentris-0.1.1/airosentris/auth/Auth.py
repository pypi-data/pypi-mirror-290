import requests
from typing import Dict, Any
from airosentris import Config


def login(url: str, token: str) -> Dict[str, Any]:
    """
    Login and initialize the pdamcc package with necessary configurations.

    Parameters:
    url (str): The API base URL.
    token (str): The authentication token.

    Raises:
    ValueError: If 'url' or 'token' is not provided.
    requests.exceptions.RequestException: If the request to the server fails.
    Exception: For other failures like unsuccessful login.

    Returns:
    Dict[str, Any]: A dictionary containing 'api_url', 'api_token', and 'agent_details'.
    """

    if not url or not token:
        raise ValueError("Both 'url' and 'token' must be provided.")

    Config.API_URL = url
    Config.API_TOKEN = token

    try:
        # Call the API to validate the user and token
        response = requests.post(
            f"{Config.API_URL}/api/v1/agent/login",
            json={"token": Config.API_TOKEN}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to server: {e}")

    result = response.json()
    if result.get('success'):
        Config.AGENT_DETAILS = result.get('data', {})
        user = Config.AGENT_DETAILS.get('user', {})
        user_name = user.get('name', 'Unknown User')
        print(
            f"pdamcc initialized with URL: {Config.API_URL}, Token: {Config.API_TOKEN}, User: {user_name}")
        return {
            'api_url': Config.API_URL,
            'api_token': Config.API_TOKEN,
            'agent_details': Config.AGENT_DETAILS
        }
    else:
        raise Exception(result.get('message', 'Login failed.'))