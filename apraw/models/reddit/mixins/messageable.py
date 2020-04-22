from ....const import API_PATH


class MessageableMixin:

    async def message(self, subject, message, from_subreddit=None):
        data = {
            "subject": subject,
            "text": message,
            "to": "{}{}".format(
                getattr(self.__class__, "MESSAGE_PREFIX", ""), self
            ),
        }
        if from_subreddit:
            data["from_sr"] = str(from_subreddit)
        await self._reddit.post(API_PATH["compose"], data=data)