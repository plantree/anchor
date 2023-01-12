"""
Task

Task for Tencent Career (https://careers.tencent.com/jobopportunity.html)
"""
from engine.requester import *
from engine.responser import *
from engine.task import *
from engine.dataitem import *
from engine.exporter import *
from engine.processor import *

class TecentCareerDataModel(DataModel):
    """
    Data model for Tecent Career
    """
    def __init__(self):
        super().__init__("tecent-career")
        technology = DataItem("number")
        self.addDataItem(technology)

class TecentCareerProcessor(Processor):
    """
    Processor for Tecent Career
    """
    def __init__(self):
        super().__init__("tecent-career")
    
    async def process(self, responser):
        if responser.status() != 200:
            raise Exception("responser status is not 200")
        datamodel = TecentCareerDataModel()
        datamodel['number'] = responser.json()['Data']['Count']
        return datamodel

class TecentCareerTask(Task):
    """
    Task for Tecent Career
    """
    def __init__(self, url, filename):
        requester = GetRequester(url)
        processor = TecentCareerProcessor()
        exporter = FileExporter("tecent-career", filename)
        super().__init__("tecent-career", requester, processor, exporter)