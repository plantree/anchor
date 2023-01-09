"""
Processor

Convert request to data item
"""
import dataitem
import responser

class Processor(object):
    """
    Base class for processor
    """
    def __init__(self, name, responser):
        self._name = name + "-processor"
        self._input = responser 
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    
    # should return a data item
    async def process(self):
        raise NotImplementedError
    
