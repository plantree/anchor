"""
Requester

issue a network request to get data
"""
import engine.responser as responser
from engine.utils import *
import aiohttp


class Requester(object):
    """
    Base class for requester
    """
    def __init__(self, name, url):
        self._name = name + "-requester"
        self._url = url
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    
    # should return Responser
    async def request(self):
        raise NotImplementedError

class GetRequester(Requester):
    """
    Requester for GET
    """
    def __init__(self, url):
        super().__init__("get", url)
        
    async def request(self):
        headers = {
            'User-Agent': get_user_agent()
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url, headers=headers) as resp:
                return responser.Responser(resp.status, await resp.text(), await resp.json())