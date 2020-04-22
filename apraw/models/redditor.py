from datetime import datetime


class Redditor:

    def __init__(self, reddit, data):
        self.reddit = reddit
        self.data = data

        self.name = data["name"]

        if "is_suspended" not in data or not data["is_suspended"]:
            self.id = data["id"]
            self.is_suspended = False
            self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

            self.is_employee = data["is_employee"]
            self.is_friend = data["is_friend"]
            self.verified = data["verified"]
            self.is_gold = data['is_gold']
            self.is_mod = data["is_mod"]
            self.has_verified_email = data["has_verified_email"]

            self.link_karma = data["link_karma"]
            self.comment_karma = data["comment_karma"]
        else:
            self.is_suspended = True

    def __str__(self):
        return self.name

    async def message(self, subject, text, from_sr=""):
        return await self.reddit.message(self.name, subject, text, from_sr)
