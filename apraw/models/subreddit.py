import aiohttp
import asyncio


async def fetch_sub_data(name):
    async with aiohttp.ClientSession() as cs, cs.get(f'https://reddit.com/r/{name}/about/.json') as resp:
        data = await resp.json()
    return data


class Subreddits:

    def __init__(self, reddit):
        self.reddit = reddit
        self.data = asyncio.create_task(fetch_sub_data(reddit))

    @property
    def icon_img(self):
        return self.data['data']['icon_img']

    async def new(self, limit=25, **kwargs):
        async for s in self.reddit.get_listing("/subreddits/new", limit, **kwargs):
            pass
            # TODO: Finish this
