"""
Bilibili career task

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

class BilibiliCareerProcessor(Processor):
    """
    Processor for Bilibili Career
    """
    def __init__(self):
        super().__init__("bilibili-career")

    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        data = responser.json()
        datamodel = DataModel("bilibili-career")
        for item in data:
            datamodel.addDataItem(DataItem(item, data[item]))
        return datamodel
    
class BilibiliCareerRequester(Requester):
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
            async with page.expect_response('https://jobs.bilibili.com/api/srs/position/positionList') as response_info:
                await page.goto(self._url)
            response = await response_info.value
            if not response.ok:
                self._status = False 
            else:
                self._data['total'] = (await response.json())['data']['total']
            
            # items
            last_value = 0
            await page.wait_for_load_state('networkidle')
            parent_div = page.locator('div', has_text='职位类别').first
            items = await parent_div.locator('div.checkbox-item').all()
            for item in items:
                name = await item.inner_text()
                async with page.expect_response('https://jobs.bilibili.com/api/srs/position/positionList') as response_info:
                    await item.click()
                response = await response_info.value
                if not response.ok:
                    self._status = False 
                else:
                    count = (await response.json())['data']['total']
                    self._data[name] = count - last_value 
                    last_value = count
            
            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)


class BilibiliCareerTask(Task):
    """
    Bilibili career task
    """
    def __init__(self, url, filename):
        requester = BilibiliCareerRequester(url)
        processor = BilibiliCareerProcessor()
        exporter = FileExporter("bilibili-career", filename)
        super().__init__("bilibili-career", requester, processor, exporter)

if __name__ == '__main__':
    requester = BilibiliCareerRequester("https://jobs.bilibili.com/social/positions?type=3")
    asyncio.get_event_loop().run_until_complete(requester.request())