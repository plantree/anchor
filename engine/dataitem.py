"""
Data Item

abstract data model
"""
from typing import Dict 
import json

class DataItem(object):
    """
    Base class for DataItem
    """

    def __init__(self, key, value=None):
        self._name = key + "-dataitem"
        self._key = key
        self._value = value

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def key(self):
        return self._key
    
    def value(self):
        return self._value
    
    def set(self, value):
        self._value = value

class DataModel(object):
    """
    Base class for DataModel
    """
    def __init__(self, name):
        self._name = name + "-datamodel"
        self._items = []
        self._fields = []
    
    def __getitem__(self, key):
        return self._items[self._fields.index(key)]
    
    def __setitem__(self, key, value):
        if key in self._fields:
            self._items[self._fields.index(key)].set(value)
        else:
            raise KeyError(f"{self.__class__.__name__} does not support field: {key}")
    
    def __iter__(self):
        return iter(self._items)
    
    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name
    
    def addDataItem(self, item):
        self._items.append(item)
        self._fields.append(item.key())
    
    def keys(self):
        return self._fields

    def to_data(self):
        return [{item.key(): item.value()} for item in self._items]