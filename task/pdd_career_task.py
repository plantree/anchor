"""
Pdd career task

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

class PddCareerProcessor(Processor):
    """
    Processor for Pdd Career
    """
    def __init__(self):
        super().__init__("pdd-career")

    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        data = responser.json()
        datamodel = DataModel("pdd-career")
        for item in data:
            datamodel.addDataItem(DataItem(item, data[item]))
        return datamodel

class PddCareerRequester(Requester):
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
            async with page.expect_response('https://careers.pinduoduo.com/api/recruit/position/list') as response_info:
                await page.goto(self._url)
            response = await response_info.value
            if not response.ok:
                self._status = False 
            else:
                self._data['total'] = (await response.json())['result']['total']    

            # items
            await page.wait_for_load_state('networkidle')
            parent_div = page.locator('div.rocket-card-body', has_text='职位类别').first 
            items = await parent_div.locator('div.tag-text').all()
            for item in items:
                name = await item.inner_text()
                if name == '全部':
                    continue 
                async with page.expect_response('https://careers.pinduoduo.com/api/recruit/position/list') as response_info:
                    await item.click()
                response = await response_info.value
                if not response.ok:
                    self._status = False
                else:
                    count = (await response.json())['result']['total'] 
                    self._data[name] = count
            
            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)

class PddCareerTask(Task):
    """
    Pdd career task
    """
    def __init__(self, url, filename):
        requester = PddCareerRequester(url)
        processor = PddCareerProcessor()
        exporter = FileExporter("pdd-career", filename)
        super().__init__("pdd-career", requester, processor, exporter)
    
if __name__ == '__main__':
    requester = PddCareerRequester("https://careers.pinduoduo.com/jobs")
    asyncio.get_event_loop().run_until_complete(requester.request())