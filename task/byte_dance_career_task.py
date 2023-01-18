"""
ByteDance career task

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

class ByteDanceCareerDataModel(DataModel):
    """
    Data model for ByteDance Career
    """
    def __init__(self):
        super().__init__("bytedance-career")
        jobs = DataItem("jobs")
        self.addDataItem(jobs)

class ByteDanceCareerProcessor(Processor):
    """
    Processor for ByteDance Career
    """
    def __init__(self):
        super().__init__("bytedance-career")
    
    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        datamodel = ByteDanceCareerDataModel()
        datamodel['jobs'] = responser.json()
        return datamodel
    
class ByteDanceCareerRequester(Requester):
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
            await page.wait_for_load_state('domcontentloaded')
            categories = await page.query_selector_all('div.TreeFilterCategory li')
            for category in categories:
                item = await category.inner_text()
                async with page.expect_response('https://jobs.bytedance.com/api/v1/search/job/posts*') as response_info:
                    await category.click()
                response = await response_info.value
                json_body = await response.json()
                if json_body['code'] == 0 and 'data' in json_body:
                    self._data[item] = json_body['data']['count']
                else:
                    self._status = False
                async with page.expect_response('https://jobs.bytedance.com/api/v1/search/job/posts*') as response_info:
                    await category.click()
                await page.wait_for_load_state('domcontentloaded')

            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)

class ByteDanceCareerTask(Task):
    """
    ByteDance career task
    """
    def __init__(self, url, filename):
        requester = ByteDanceCareerRequester(url)
        processor = ByteDanceCareerProcessor()
        exporter = FileExporter("bytedance-career", filename)
        super().__init__("bytedance-career", requester, processor, exporter)

if __name__ == "__main__":
    requester = ByteDanceCareerRequester("https://jobs.bytedance.com/experienced/position")
    asyncio.get_event_loop().run_until_complete(requester.request())