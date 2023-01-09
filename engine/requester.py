"""
Requester

issue a network request to get data
"""
import responser

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