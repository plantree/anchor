"""
Anchor Engine

schedule all tasks
"""
import asyncio 
from engine.logger import log
from engine.task import *

class AnchorEngine(object):
    """
    Crawler engine
    """
    def __init__(self):
        self._name = "anchor-engine"
        self._tasks = []
        self._running = False
    
    def __repr__(self):
        return self._name
    
    def __str__(self):
        return self._name
    
    def addTask(self, tasks):
        self._tasks.append(tasks)
    
    def start(self):
        self._running = True
        loop = asyncio.get_event_loop()
        tasks = []
        for item in self._tasks:
            tasks.append(item.run())
        loop.run_until_complete(asyncio.wait(tasks))
        count = len(tasks)
        success = 0
        for item in self._tasks:
            log.info(item.status())
            if item.status() == TaskStatus.DONE:
                success += 1
        log.info("task done, total: %d, success: %d, rate: %f%%" % (count, success, success / count * 100))
        loop.close()
        return 0 if success == count else -1