"""
Meituan career task

based on palywright
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

class MeituanCareerProcessor(Processor):
    """
    Processor for Meituan Career
    """
    def __init__(self):
        super().__init__("meituan-career")
    
    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        data = responser.json()
        datamodel = DataModel("meituan-career")
        for item in data:
            datamodel.addDataItem(DataItem(item, data[item]))
        return datamodel

class MeituanCareerRequester(Requester):
    """
    A wrapper for playwright
    """
    def __init__(self, url):
        self._name = "playwright"
        self._url = url 
        self._data = {}
        self._status = True 
    
    async def request(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            async with page.expect_response('https://zhaopin.meituan.com/api/official/job/getJobList') as response_info:
                await page.goto(self._url)
            response = await response_info.value
            if not response.ok:
                self._status = False 
            else:
                self._data['total'] = (await response.json())['data']['page']['totalCount']
            
            #items
            last_value = 0
            await page.wait_for_load_state('domcontentloaded')
            parent_div = page.locator('div.category').first 
            items = await parent_div.locator('div.condition_item_content').all()
            for item in items:
                name_div = item.locator('div.condition_item_subtitle').first
                name = await name_div.inner_text()
                await item.click()
                await page.wait_for_load_state('domcontentloaded')
                async with page.expect_response('https://zhaopin.meituan.com/api/official/job/getJobList') as response_info:
                    await item.locator('div.condition_item_filter_item', has_text='全部').first.click()
                response = await response_info.value
                if not response.ok:
                    self._status = False 
                else:
                    count = (await response.json())['data']['page']['totalCount'] 
                    self._data[name] = count - last_value 
                    last_value = count
            
            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)

class MeituanCareerTask(Task):
    """
    Task for Meituan Career
    """
    def __init__(self, url, filename):
        requester = MeituanCareerRequester(url)
        processor = MeituanCareerProcessor()
        exporter = FileExporter("meituan-career", filename)
        super().__init__("meituan-career", requester, processor, exporter)

if __name__ == '__main__':
    requester = MeituanCareerRequester("https://zhaopin.meituan.com/web/social")
    asyncio.get_event_loop().run_until_complete(requester.request())