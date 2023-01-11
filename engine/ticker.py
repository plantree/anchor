"""
Ticker

a ticker is a class that is responsible for keeping track of the current
"""
import time

class Ticker(object):
    """
    A simple ticker
    """
    def __init__(self):
        self._name = "ticker"
        self._current = 0
        self._next = 0

    def checkin(self):
        self._current = int(round(time.time() * 1000))
    
    def checkout(self):
        self._next = int(round(time.time() * 1000))
        delta = self._next - self._current
        self._current = self._next
        return delta