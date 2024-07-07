"""
360 career task

based on playwright
"""
import sys
sys.path.append('..')

import asyncio
import time
from playwright.async_api import async_playwright
from engine.logger import *
from engine.requester import *
from engine.responser import *
from engine.task import *
from engine.dataitem import *
from engine.exporter import *
from engine.processor import *

# default DataModel

class ThreeSixZeroCareerProcessor(Processor):
    """
    Processor for 360 Career
    """
    def __init__(self):
        super().__init__("360-career")

    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        data = responser.json()
        datamodel = DataModel("360-career")
        for item in data:
            datamodel.addDataItem(DataItem(item, data[item]))
        return datamodel

class ThreeSixZeroCareerRequester(Requester):
    """
    A wrapper for playwright
    """
    def __init__(self, url):
        self._name = "playwrighter"
        self._url = url
        self._data = {}
        self._status = True
    
    async def request(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            async with page.expect_response('https://hr.360.cn/v2/index/getlistsearch') as response_info:
                await page.goto(self._url)
            response = await response_info.value
            if not response.ok:
                self._status = False 
            else:
                data = await response.json()
                self._data['total'] = data['count']
                # items
                items = {}
                for item in data['data']:
                    category = item['type']
                    if category in items:
                        items[category] += 1
                    else:
                        items[category] = 0
                for item in items:
                    self._data[item] = items[item]

            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)

class ThreeSixZeroCareerTask(Task):
    """
    ThreeSixZero career task
    """
    def __init__(self, url, filename):
        requester = ThreeSixZeroCareerRequester(url)
        processor = ThreeSixZeroCareerProcessor()
        exporter = FileExporter("360-career", filename)
        super().__init__("360-career", requester, processor, exporter)
    
if __name__ == '__main__':
    requester = ThreeSixZeroCareerRequester("https://hr.360.cn/hr/list")
    asyncio.get_event_loop().run_until_complete(requester.request())
