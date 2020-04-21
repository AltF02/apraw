import aiohttp
from datetime import datetime, timedelta

from .models.subreddit import Subreddits


class Reddit():

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
        self.token_expires = datetime.now()

    async def get_header(self):
        if self.token_expires <= datetime.now():
            url = "https://www.reddit.com/api/v1/access_token"
            data = {
                "username": self.username,
                "password": self.password
            }

            auth = aiohttp.BasicAuth(login=self.client_id, password=self.client_secret)
            async with aiohttp.ClientSession(auth=auth) as session:
                async with session.post(url, data=data) as resp:
                    if resp.status == 200:
                        self.access_data = await resp.json()
                        self.token_expires = datetime.now() + timedelta(seconds=self.access_data['expires_in'])
                    else:
                        raise Exception("Invalid data")

        return {
            "Authorization": f"{self.access_data['token_type']} {self.access_data['access_token']}",
            "User-Agent": self.user_agent
        }

    async def get_request(self, endpoint, limit, **kwargs):
        kwargs['raw_json'] = 1
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]
        url = "https://oauth.reddit.com{endpoint}?" + '&'.join(params)

        async with aiohttp.ClientSession() as session:
            headers = await self.get_header()
            async with session.get(url, headers=headers) as resp:
                return await resp.json()

    async def get_listing(self, endpoint, limit, **kwargs):
        last = None
        while True:
            kwargs['limit'] = limit if limit is not None else 100
            if last is not None:
                kwargs["after"] = last
            req = await self.get_request(endpoint, **kwargs)
            if len(req["data"]["children"]) <= 0:
                break
            for i in req["data"]["children"]:
                if i["kind"] in [self.link_kind, self.subreddit_kind]:
                    last = i["data"]["name"]
                if limit is not None:
                    limit -= 1
                yield i
            if limit is not None and limit < 1:
                break

    async def request_post(self, endpoint, data, **kwargs):
        kwargs['raw_json'] = 1
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]
        url = "https://oauth.reddit.com{endpoint}?" + '&'.join(params)

        async with aiohttp.ClientSession as session:
            headers = await self.get_header()
            async with session.post(url, data=data, headers=headers) as resp:
                return await resp.json()

    async def message(self, to, subject, text, from_sr=""):
        data = {
            "subject": subject,
            "text": text,
            "to": to
        }
        if from_sr != "": data["from_sr"] = from_sr
        resp = await self.request_post("/api/compose", data)
        return resp["success"]
