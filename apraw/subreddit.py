import aiohttp
import asyncio


async def fetch_sub_data(name):
    async with aiohttp.ClientSession() as cs, cs.get(f'https://reddit.com/r/{name}/about/.json') as resp:
        data = await resp.json()
    return data


class Subreddit:

    def __init__(self, name):
        self.name = name
        self.data = asyncio.create_task(fetch_sub_data(name))

    @property
    def icon_img(self):
        return self.data['data']['icon_img']
