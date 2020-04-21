import aiohttp

from .subreddits import Subreddits


class reddit():

    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        self.comment_kind = "t1"
        self.account_kind = "t2"
        self.link_kind = "t3"
        self.message_kind = "t4"
        self.subreddit_kind = "t5"
        self.award_kind = "t6"

        self.subreddits = Subreddits(self)
        self.access_data = None
