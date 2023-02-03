#!/usr/bin/env python3
from engine.anchorengine import AnchorEngine
from engine.logger import log
from datetime import datetime
from task.tecent_career_task import *
from task.baidu_career_task import *
from task.alibaba_career_task import *
from task.byte_dance_career_task import *
from task.jd_career_task import *
from task.bilibili_career_task import *
from task.meituan_career_task import *
from task.netease_career_task import *
from task.pdd_career_task import *
from task.three_six_zero_career_task import *

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

    # task 12
    baidu_career_url = "https://talent.baidu.com/jobs/social-list"
    engine.addTask(BaiduCareerTask(baidu_career_url, "baidu-career.json"))

    # task 13
    alibaba_career_url = "https://talent.alibaba.com/off-campus/position-list?lang=zh"
    engine.addTask(AlibabaCareerTask(alibaba_career_url, "alibaba-career.json"))

    # task 14
    byte_dance_career_url = "https://jobs.bytedance.com/experienced/position"
    engine.addTask(ByteDanceCareerTask(byte_dance_career_url, "byte-dance-career.json"))
    
    # task 15
    jd_career_url = "https://zhaopin.jd.com/web/job/job_info_list/3"
    engine.addTask(JDCarerrTask(jd_career_url, "jd-career.json"))

    # task 16 
    bilibili_career_url = "https://jobs.bilibili.com/social/positions?type=3"
    engine.addTask(BilibiliCareerTask(bilibili_career_url, "bilibili-career.json"))

    # task 17
    meituan_career_url = 'https://zhaopin.meituan.com/web/social'
    engine.addTask(MeituanCareerTask(meituan_career_url, "meituan-career.json"))

    # # task 18
    # netease_career_url = 'https://hr.163.com/job-list.html?workType=0'
    # engine.addTask(NeteaseCareerTask(netease_career_url, "netease-career.json"))

    # # task 19
    # pdd_career_url = 'https://careers.pinduoduo.com/jobs'
    # engine.addTask(PddCareerTask(pdd_career_url, "pdd-career.json"))

    # task 20
    three_six_zero_career_url = 'http://hr.360.cn/hr/list'
    engine.addTask(ThreeSixZeroCareerTask(three_six_zero_career_url, "360-career.json"))

    status = engine.start()
    log.info("Anchor stopped")
    exit(status)