"""
Exporter

export data item
"""
import asyncio
import aiofiles as aiof

class Exporter(object):
    """
    Base class for exporter
    """
    def __init__(self, name, dataitem):
        self._name = name + "-exporter"
        self._input = dataitem
    
    async def export(self):
        raise NotImplementedError

class FileExporter(Exporter):
    """
    File exporter
    """
    def __init__(self, name, data, filename):
        super(FileExporter, self).__init__(name, data)
        self._filename = filename
    
    async def export(self):
        async with aiof.open(self._filename, "w") as f:
            await f.write(self._input.toJson())
            await f.flush()