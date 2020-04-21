import aiohttp


class Subreddit:

    def __init__(self, subreddit):
        self.subreddit = subreddit

    @property
    async def mod(self):
        return SubredditModeration(self)


class SubredditModeration:

    def __init__(self, subreddit):
        self.subreddit = subreddit

    async def modqueue(self, **kwargs):


