import aiohttp


class Subreddit:

    def __init__(self, subreddit):
        self.subreddit = subreddit

    @property
    async def banned(self):
        return SubredditRelationship(self, "banned")

    @property
    def contributor(self):
        return ContributorRelationship(self, "contributor")

    @property
    async def flair(self):
        return SubredditFlair(self)

    @property
    async def mod(self):
        return SubredditModeration(self)

    @property
    async def moderator(self):
        return ModeratorRelationship(self, "moderator")


class SubredditFlair:

    async def __call__(self):
        pass

    def __init__(self, subreddit): \
        self.subreddit = subreddit


class SubredditRelationship:

    def __init__(self, subreddit, relationship):
        self.relationship = relationship
        self.subreddit = subreddit


class SubredditModeration:

    def __init__(self, subreddit):
        self.subreddit = subreddit


class ContributorRelationship(SubredditRelationship):

    async def leave(self):
        pass


class ModeratorRelationship(SubredditRelationship):

    async def __call__(self, redditor=None):
        params = {} if redditor is None else {"user": redditor}


class Modmail:

    async def __call__(self, id=None, mark_read=False):
        pass
