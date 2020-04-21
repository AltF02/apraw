import aiohttp

from .subreddits import Subreddits

class reddit():

    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
