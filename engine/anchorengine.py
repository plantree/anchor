"""
Anchor Engine

schedule all tasks
"""
import asyncio 

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
        loop.close()