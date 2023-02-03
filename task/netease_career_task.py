"""
Netease career task

based on playwright
"""
import sys
sys.path.append('..')

import asyncio
from playwright.async_api import async_playwright
from engine.logger import *
from engine.requester import *
from engine.responser import *
from engine.task import *
from engine.dataitem import *
from engine.exporter import *
from engine.processor import *

# default DataModel

class NeteaseCareerProcessor(Processor):
    """
    Processor for Netease Career
    """
    def __init__(self):
        super().__init__("netease-career")

    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        data = responser.json()
        datamodel = DataModel("netease-career")
        for item in data:
            datamodel.addDataItem(DataItem(item, data[item]))
        return datamodel

class NeteaseCareerRequester(Requester):
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
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(self._url)
            content = await page.content()
            print(content.title())
            async with page.expect_response('https://hr.163.com/api/hr163/position/queryPage', timeout=100000) as response_info:
                await page.goto(self._url)
            response = await response_info.value
            if not response.ok:
                self._status = False 
            else:
                self._data['total'] = (await response.json())['data']['total']    

            # items
            await page.wait_for_load_state('networkidle')
            parent_div = page.locator('div.check-box-item', has_text='职位类别').first 
            items = await parent_div.locator('div.radio-item').all()
            for item in items:
                name = await item.inner_text()
                if name == '不限':
                    continue 
                async with page.expect_response('https://hr.163.com/api/hr163/position/queryPage', timeout=100000) as response_info:
                    await item.click()
                response = await response_info.value
                if not response.ok:
                    self._status = False
                else:
                    count = (await response.json())['data']['total'] 
                    self._data[name] = count
            
            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)

class NeteaseCareerTask(Task):
    """
    Netease career task
    """
    def __init__(self, url, filename):
        requester = NeteaseCareerRequester(url)
        processor = NeteaseCareerProcessor()
        exporter = FileExporter("netease-career", filename)
        super().__init__("netease-career", requester, processor, exporter)
    
if __name__ == '__main__':
    requester = NeteaseCareerRequester("https://hr.163.com/job-list.html?workType=0")
    asyncio.get_event_loop().run_until_complete(requester.request())