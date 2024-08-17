
class Config:
    API_URL = None
    API_TOKEN = None
    AGENT_DETAILS = None


from .auth.Auth import login
from .projects.Project import init

import airosentris.datasets.social_comment