import aiohttp
from .exceptions import *
from .const import __version__, TIMEOUT


class Requestor(object):

    def __getattr__(self, attribute):
        if attribute.startswith('__'):
            raise AttributeError
        return getattr(self._http, attribute)

    def __init__(self, user_agent, oauth_url='https://oauth.reddit.com',
                 reddit_url='https://www.reddit.com', session=None):
        if user_agent is None or len(user_agent) < 7:
            raise InvalidInvocation('user_agent is not descriptive')

        self._http = session or aiohttp.ClientSession()
        self._http.headers['user_agent'] = f'{user_agent} aprawcore/{__version__}'

        self.oauth_url = oauth_url
        self.reddit_url = reddit_url

    async def close(self):
        return await self._http.close()

    async def request(self, *args, **kwargs):
        try:
            async with self._http.request(*args, timeout=TIMEOUT, **kwargs) as resp:
                return resp
        except Exception as exc:
            raise RequestException(exc, args, kwargs)
