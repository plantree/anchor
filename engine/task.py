"""
Task

basic scheduling unit
"""
from enum import Enum 

class TaskStatus(Enum):
    """
    Task status
    """
    INIT = 0
    REQUESTER = 1
    PROCESSOR = 2
    EXPORTER = 3
    DONE = 3
    FAILED = 4

class Task(object):
    """
    Base class for task
    """
    def __init__(self, name, requester, processor, exporter):
        self._name = name + "-task"
        self._requester = requester
        self._processor = processor
        self._exporter = exporter
        self._status = TaskStatus.INIT

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name
    
    def status(self):
        return self._status
    
    async def run(self):
        self._status = TaskStatus.REQUESTER
        self._responser = self._requester.request()
        if self._responser.status() == 200:
            self._status = TaskStatus.PROCESSOR
            self._dataitem = await self._processor.process(self._responser)
            self._status = TaskStatus.EXPORTER
            await self._exporter.export(self._dataitem)
            self._status = TaskStatus.DONE
        else:
            self._status = TaskStatus.FAILED
        return self._status