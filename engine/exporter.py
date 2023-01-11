"""
Exporter

export data item
"""
import asyncio
import aiofiles as aiof
import json
import os
import time

from engine.utils import *

class Exporter(object):
    """
    Base class for exporter
    """
    def __init__(self, name):
        self._name = name + "-exporter"
    
    async def export(self):
        raise NotImplementedError

class FileExporter(Exporter):
    """
    File exporter
    """
    def __init__(self, dir, filename):
        super().__init__("file")
        today = get_today()
        self._dir = os.path.join('data', dir, today)
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)
        self._filename = filename
    
    async def export(self, data):
        filename = os.path.join(self._dir, self._filename)
        async with aiof.open(filename, "w") as f:
            await f.write(json.dumps(data.to_data()))
            await f.flush()