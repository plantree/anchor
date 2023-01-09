"""
Responser

store information of response
"""
class Responser(object):
    """
    Base class for responser
    """
    def __init__(self, status, body):
        self._name = "responser"
        self._status = status
        self._body = body
    
    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name
    
    def status(self):
        return self._status 

    def body(self):
        return self._body 
    