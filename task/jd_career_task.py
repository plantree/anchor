"""
JD career task

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

class JDCareerProcessor(Processor):
    """
    Processor for JD Career
    """
    def __init__(self):
        super().__init__("jd-career")
    
    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        data = responser.json()
        datamodel = DataModel("jd-career")
        for item in data:
            datamodel.addDataItem(DataItem(item, data[item]))
        return datamodel

class JDCareerRequester(Requester):
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
            switch = page.locator('div.suggess-sel').first
            await switch.click()
            await page.wait_for_load_state('domcontentloaded')
            # find items
            items = await page.locator('div#jobType li').all()
            last_value = 0
            for item in items:
                name = await item.inner_text()
                if name == '全部':
                    continue
                async with page.expect_response('https://zhaopin.jd.com/web/job/job_count') as response_info:
                    await item.locator('input').first.click()
                response = await response_info.value
                if not response.ok:
                    self._status = False
                    break
                count = int(await response.text())
                self._data[name] = count - last_value
                last_value = count
            
            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)

class JDCarerrTask(Task):
    """
    Task for JD Career
    """
    def __init__(self, url, filename):
        requester = JDCareerRequester(url)
        processor = JDCareerProcessor()
        exporter = FileExporter("jd-career", filename)
        super().__init__("jd-career", requester, processor, exporter)

if __name__ == "__main__":
    requester = JDCareerRequester("https://zhaopin.jd.com/web/job/job_info_list/3")
    asyncio.get_event_loop().run_until_complete(requester.request())
