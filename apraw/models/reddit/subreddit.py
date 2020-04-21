import aiohttp


class Subreddit:

    def __init__(self, subreddit):
        self.subreddit = subreddit

    @property
    async def flair(self):
        return SubredditFlair(self)

    @property
    async def mod(self):
        return SubredditModeration(self)

    @property
    async def moderator(self):
        return ModeratorRelationship(self, "moderator")

class SubredditRelationship:

    def __init__(self, subreddit, relationship):
        self.relationship = relationship
        self.subreddit = subreddit

class SubredditModeration:

    def __init__(self, subreddit):
        self.subreddit = subreddit


class ModeratorRelationship(SubredditRelationship):

    async def __call__(self, redditor=None):
        params = {} if redditor is None else {"user": redditor}
