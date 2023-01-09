"""
Data Item

abstract data model
"""
from typing import Dict 
import json

class Item(object):
    """
    Base class for Item
    """
    def __init__(self, value=None):
        self._value = value

    def __repr__(self):
        return self._value.__repr__()

    def __str__(self):
        return self._value.__repr__()
    
    def value(self):
        return self._value
    
    def set(self, value):
        self._value = value
    
    def toJSON(self):
        return json.dumps(self)

class DataItem(object):
    """
    Base class for DataItem
    """

    def __init__(self, name):
        self._name = name + "-dataitem"
        self._values = Dict(str, Item)
    
    def __getitem__(self, key):
        if key in self._values:
            return self._values[key]
        else:
            return None
    
    def __setitem__(self, key, value):
        self._values[key] = value
    
    def __iter__(self):
        return iter(self._values)
    
    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    
    def addItem(self, key, item):
        self._values[key] = item.value()

    def keys(self):
        return self._values.keys()
    
    def values(self):
        return self._values.values()

    def toJSON(self, *args, **kwargs):
        return json.dumps(self._values, *args, **kwargs)