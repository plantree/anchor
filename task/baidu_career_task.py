"""
Baidu career task

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

class BaiduCareerDataModel(DataModel):
    """
    Data model for Baidu Career
    """
    def __init__(self):
        super().__init__("baidu-career")
        jobs = DataItem("jobs")
        self.addDataItem(jobs)

class BaiduCareerProcessor(Processor):
    """
    Processor for Baidu Career
    """
    def __init__(self):
        super().__init__("baidu-career")
    
    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        datamodel = BaiduCareerDataModel()
        datamodel['jobs'] = responser.json()
        return datamodel
        
class BaiduCareerRequester(Requester):
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
            async with page.expect_response('https://talent.baidu.com/httservice/getPostListNew') as response_info:
                await page.goto(self._url)
            response = await response_info.value
            if response.ok:
                json_body = await response.json()
                if 'data' in json_body and 'total' in json_body['data']:
                    self._data['total'] = int(json_body['data']['total'])
                else:
                    self._status = False
            else:
                self._status = False
            last_value = 0
            for item in ['技术', '产品', '政企行业解决方案和服务', '专业服务和管理支持']:
                job = page.locator('span.brick-checkbox-label', has_text=item).first
                async with page.expect_response('https://talent.baidu.com/httservice/getPostListNew') as response_info:
                    await job.click()
                response = await response_info.value
                json_body = await response.json()
                if response.ok:
                    if 'data' in json_body and 'total' in json_body['data']:
                        self._data[item] = int(json_body['data']['total']) - last_value
                        last_value += self._data[item]
                    else:
                        self._status = False
                else:
                    self._status = False
            await browser.close()
            log.info(self._data)
            return Responser(200 if self._status else 500, json.dumps(self._data), self._data)

class BaiduCareerTask(Task):
    """
    Task for Baidu Career
    """
    def __init__(self, url, filename):
        requester = BaiduCareerRequester(url)
        processor = BaiduCareerProcessor()
        exporter = FileExporter("baidu-career", filename)
        super().__init__("baidu-career", requester, processor, exporter)


if __name__ == '__main__':
    # pw = PlayWrighter()
    # asyncio.get_event_loop().run_until_complete(pw.request('https://talent.baidu.com/jobs/social-list'))
    requester = BaiduCareerRequester('https://talent.baidu.com/jobs/social-list')
    asyncio.get_event_loop().run_until_complete(requester.request())