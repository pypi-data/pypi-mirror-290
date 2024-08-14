import requests
from airosentris import Config


def login(config):
    """
    Login and initialize the pdamcc package with necessary configurations.

    Parameters:
    config (dict): A dictionary containing configuration keys 'url' and 'token'.

    Raises:
    ValueError: If 'url' or 'token' is not provided in the config.

    Returns:
    dict: A dictionary containing 'api_url', 'api_token', and 'agent_details'.
    """
    if 'url' not in config or 'token' not in config:
        raise ValueError("Config must include 'url' and 'token'.")

    Config.API_URL = config['url']
    Config.API_TOKEN = config['token']

    # Call the API to validate the user and token
    response = requests.post(
        f"{Config.API_URL}/api/v1/agent/login",
        json={"token": Config.API_TOKEN}
    )

    if response.status_code == 200:
        result = response.json()
        if result['success']:
            Config.AGENT_DETAILS = result['data']
            user = Config.AGENT_DETAILS['user']
            print(
                f"pdamcc initialized with URL: {Config.API_URL}, Token: {Config.API_TOKEN}, User: {user['name']}")
            return {
                'api_url': Config.API_URL,
                'api_token': Config.API_TOKEN,
                'agent_details': Config.AGENT_DETAILS
            }
        else:
            raise Exception(result['message'])

    else:
        raise Exception("Failed to connect server.")