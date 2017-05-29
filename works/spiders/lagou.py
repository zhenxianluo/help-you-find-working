# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import Spider
import logging, json, math, re
from scrapy.selector import Selector 
from works.items import WorksItem

class LagouSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["lagou.com"]
    download_delay = 1 
    base_url = 'https://www.lagou.com/jobs/positionAjax.json'
    base_data = { 
                'px': 'default',
                'city': '上海',
                'needAddtionalResult': 'false',
                'kd': 'Python爬虫',
                'first': 'first',
                'pn': '1' 
                }
    def start_requests(self):
        url = self.parse_url(self.base_url, self.base_data)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse_url(self, url, data):
        haha = []
        for key in data:
            haha.append(key+'='+str(data[key]))
        return url + '?' + '&'.join(haha)

    def parse(self, response):
        print '-'*50
        print response.url
        data = json.loads(response._body)
        max_pages = int(math.ceil(data['content']['positionResult']['totalCount']/float(data['content']['pageSize'])))
        urls = []
        for i in range(1, max_pages+1):
            self.base_data['pn'] = i 
            urls.append(self.parse_url(self.base_url,self.base_data))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self, response):
        res = json.loads(response._body)
        results = res['content']['positionResult']['result']
        hrconts = res['content']['hrInfoMap']
        items = []
        for rt in results:
            item = WorksItem()
            item['origin'] = self.name
            item['positionName'] = rt['positionName'] #招聘的职位: 如高级Python工程师
            item['workYear'] = rt['workYear'] #工作年限: 如3-5年
            item['education'] = rt['education'] #毕业要求: 如本科
            item['jobNature'] = rt['jobNature'] #全职或兼职
            item['createTime'] = rt['createTime'] #创建时间
            item['companyShortName'] = rt['companyShortName'] #公司简称
            item['city'] = rt['city'] #城市
            item['salary'] = rt['salary'] #工资水平: 如15k-25k
            item['positionAdvantage'] = rt['positionAdvantage'] #氛围标签: 如下午茶
            item['industryField'] = rt['industryField'] #公司营业领域: 如>移动互联网
            item['financeStage'] = rt['financeStage'] #融资级别: 如成熟型(D轮及以上)
            item['companyLabelList'] = '/'.join(rt['companyLabelList']) if rt['companyLabelList'] is not None else None #福利: 如节日礼物,绩效奖金
            item['district'] = rt['district'] #县区
            item['companySize'] = rt['companySize'] #公司规模: 如2000人及>以上
            item['companyFullName'] = rt['companyFullName'] #公司全名
            item['businessZones'] = '/'.join(rt['businessZones']) if rt['businessZones'] is not None else None #附近定位: 如人民广场
            item['firstType'] = rt['firstType'] #第一分类: 如技术
            item['secondType'] = rt['secondType'] #第二分类: 如后端开发
            posId = str(rt['positionId'])
            item['userPositionName'] = hrconts[posId]['positionName'] #职>位: 如hr
            item['phone'] = hrconts[posId]['phone']
            item['receiveEmail'] = hrconts[posId]['receiveEmail']
            item['realName'] = hrconts[posId]['realName'] #真实姓名
            items.append(scrapy.Request(url='https://www.lagou.com/jobs/'+str(posId)+'.html', meta={'item':item}, callback=self.get_detail))
        print items
        return items

    def get_detail(self, response):
        item = response.meta['item']
        sel = Selector(response)
        item['detail'] = re.sub('[\']', '', ''.join(sel.xpath('//dd[@class="job_bt"]//p/text()').extract())) #职位要求
        item['address'] = re.sub('[\n -]', '', ''.join(sel.xpath('//div[@class="work_addr"]/text()').extract())) #详细地址
        item['website'] = sel.xpath('//ul[@class="c_feature"]//a/text()').extract()[0] #官网
        return item
