#!/usr/bin/env python3
from engine.anchorengine import AnchorEngine
from engine.logger import log
from task.tecent_career_task import *
from datetime import datetime

if __name__ == '__main__':
    log.debug("Anchor starting")
    engine = AnchorEngine()
    timestamp = datetime.now().timestamp()
    # task 1
    career_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40001&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(career_url, "tecent-career-technology.json"))
    # task 2
    product_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40003&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(product_url, "tecent-career-product.json"))
    # task 3
    content_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40006&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(content_url, "tecent-career-content.json"))
    # task 4
    design_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40002&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(design_url, "tecent-career-content.json"))
    # task 5
    sale_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40005&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(sale_url, "tecent-career-sale.json"))
    # task 6
    hr_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40008&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(hr_url, "tecent-career-hr.json"))
    # task 7
    relation_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40004&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(relation_url, "tecent-career-relation.json"))
    # task 8
    invest_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=400011&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(invest_url, "tecent-career-invest.json"))
    # task 9
    finance_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40007&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(finance_url, "tecent-career-finance.json"))
    # task 10
    law_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40009&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(law_url, "tecent-career-law.json"))
    # task 11
    support_url = f"https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={timestamp}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=400010&attrId=&keyword=&pageIndex=1&pageSize=10000&language=zh-cn&area=cn"
    engine.addTask(TecentCareerTask(support_url, "tecent-career-support.json"))

    engine.start()
    log.info("Anchor stopped")