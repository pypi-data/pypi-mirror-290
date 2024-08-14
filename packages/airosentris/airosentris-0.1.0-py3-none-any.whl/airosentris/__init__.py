import json

import requests


class Config:
    API_URL = None
    API_TOKEN = None
    AGENT_DETAILS = None


from .auth.Auth import login
