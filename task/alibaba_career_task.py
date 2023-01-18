"""
Alibaba career task

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
import re

class AlibabaCareerDataModel(DataModel):
    """
    Data model for Alibaba Career
    """
    def __init__(self):
        super().__init__("alibaba-career")
        jobs = DataItem("jobs")
        self.addDataItem(jobs)

class AlibabaCareerProcessor(Processor):
    """
    Processor for Alibaba Career
    """
    def __init__(self):
        super().__init__("alibaba-career")
    
    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        datamodel = AlibabaCareerDataModel()
        datamodel['jobs'] = responser.json()
        return datamodel

class AlibabaCareerRequester(Requester):
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
            async with page.expect_response('https://talent.alibaba.com/category/list*') as response_info:
                await page.goto(self._url)
            # total jobs
            jobs = page.locator('span', has_text='个岗位')
            total_jobs_text = await jobs.inner_text()
            total_jobs = re.findall(r'\d+', total_jobs_text)
            if len(total_jobs) > 0:
                total_jobs = int(total_jobs[0])
            else:
                total_jobs = 0
                self._status = False
            self._data['total'] = total_jobs
            # items
            items = []
            response = await response_info.value
            if response.ok:
                json_body = await response.json()
                if json_body['success'] and 'content' in json_body:
                    for i in json_body['content']:
                        items.append(i['name'])
                else:
                    self._status = False
            else:
                self._status = False

            last_value = 0
            for item in items:
                input = page.locator(f'input[aria-label="{item}"]')
                async with page.expect_response('https://talent.alibaba.com/position/search*') as response_info:
                    await input.click()
                response = await response_info.value
                if response.ok:
                    json_body = await response.json()
                    if json_body['success'] and 'content' in json_body:
                        self._data[item] = json_body['content']['totalCount'] - last_value
                        last_value += self._data[item]
                    else:
                        self._status = False
                else:
                    self._status = False
            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)


class AlibabaCareerTask(Task):
    """
    Task for Alibaba Career
    """
    def __init__(self, url, filename):
        requester = AlibabaCareerRequester(url)
        processor = AlibabaCareerProcessor()
        exporter = FileExporter("alibaba-career", filename)
        super().__init__("alibaba-career", requester, processor, exporter)

if __name__ == "__main__":
    requester = AlibabaCareerRequester("https://talent.alibaba.com/off-campus/position-list?lang=zh")
    asyncio.get_event_loop().run_until_complete(requester.request())