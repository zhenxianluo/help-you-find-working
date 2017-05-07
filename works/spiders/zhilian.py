# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import Spider
import logging, json, math, datetime, re
from scrapy.selector import Selector 
from works.items import WorksItem
from bs4 import BeautifulSoup

class ZhilianSpider(scrapy.Spider):
    name = "zhilian"
    download_delay = 1
    allowed_domains = ['zhaopin.com', 'jobs.zhaopin.com', 'sou.zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7&kw=python&sm=0&isfilter=1&p=1']

    def parse(self, response):
        logging.debug('---------------------------------------------------------------------------------------------------')
        rep = Selector(response)
        urls = rep.xpath('//td[@class="zwmc"]//a[@style="font-weight: bold"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_item, meta={'url': url})
        next_page = rep.xpath('//a[@class="next-page"]')
        if len(next_page) != 0:
            url = next_page[0].xpath('@href').extract()[0]
            yield scrapy.Request(url=url, callback=self.parse)

    def get_item(self, response):
        item = WorksItem()
        soup = BeautifulSoup(response._body, 'lxml')
        fl = soup.find('div', {'class': 'fl'})
        item['positionName'] = fl.h1.string.strip()
        item['companyFullName'] = fl.h2.get_text().strip()
        item['companyLabelList'] = '/'.join([span.string.strip() for span in fl.select('div.welfare-tab-box span')])
        info = soup.find_all('ul', {'class': 'terminal-ul'})
        ss1 = info[1].find_all('strong')
        ss1_need = ['companySize', 'company_type', 'industryField', 'website', 'address']
        if len(ss1) ==4: del ss1_need[3]
        for i in range(len(ss1_need)):
            item[ss1_need[i]] = ss1[i].get_text().strip()
        ss0 = info[0].find_all('strong')
        ss0_need = ['salary', 'city', 'createTime', 'jobNature', 'workYear', 'education']
        for i in range(len(ss0_need)):
            if i == 2:
                create_date = ss0[i].get_text().strip()
                if create_date == u'昨天':
                    item[ss0_need[i]] = str(datetime.date.today() - datetime.timedelta(days=1))
                elif create_date == u'今天' or create_date == u'刚刚':
                    item[ss0_need[i]] = str(datetime.date.today())
                elif create_date == u'前天':
                    item[ss0_need[i]] = str(datetime.date.today() - datetime.timedelta(days=2))
                elif re.search('^\d{4}-\d{2}-\d{2}$', create_date) > -1:
                    item[ss0_need[i]] = create_date
                else:
                    item[ss0_need[i]] = '1900-01-01'
            else:
                item[ss0_need[i]] = ss0[i].get_text().strip()
        com_detail = soup.find('div', {'class': 'tab-cont-box'}).select('div.tab-inner-cont')
        item['detail'] = ''.join([re.sub('[\' ]', '`', p.get_text().strip()) for p in com_detail[0].select('p')])
        item['company_info'] = re.sub('[\' ]', '`', com_detail[1].select('p')[0].get_text().strip())
        return item
