"""
Task

basic scheduling unit
"""
import asyncio
from enum import Enum 
from engine.logger import log
from engine.ticker import Ticker

class TaskStatus(Enum):
    """
    Task status
    """
    INIT = 0
    REQUESTER = 1
    PROCESSOR = 2
    EXPORTER = 3
    DONE = 4
    FAILED = 5

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
        self._ticker = Ticker()

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name
    
    def status(self):
        return self._status
    
    async def run(self):
        log.info("task %s start" % self._name)
        self._ticker.checkin()
        self._status = TaskStatus.REQUESTER
        self._responser = await self._requester.request()
        delta = self._ticker.checkout()
        log.info("task [%s] get response, delta: %d ms" % (self._name, delta))
        try:
            self._status = TaskStatus.PROCESSOR
            self._datamodel = await self._processor.process(self._responser)
            delta = self._ticker.checkout()
            log.info("task [%s] process data, delta: %d ms" % (self._name, delta))
            self._status = TaskStatus.EXPORTER
            await self._exporter.export(self._datamodel)
            self._status = TaskStatus.DONE
            delta = self._ticker.checkout()
            log.info("task [%s] export data, delta: %d ms" % (self._name, delta))
        except Exception as e:
            log.warn("task [%s] failed, ex: %s" % (self._name, e))
            self._status = TaskStatus.FAILED
        log.info("task %s end, with status: %s" % (self._name, self._status))
        return self._status