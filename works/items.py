# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class WorksItem(Item):
    origin = Field() #来源
    positionName = Field() #招聘的职位: 如高级Python工程师
    workYear = Field() #工作年限: 如3-5年
    education = Field() #毕业要求: 如本科
    jobNature = Field() #全职或兼职
    createTime = Field() #创建时间
    companyShortName = Field() #公司简称
    city = Field() #城市
    salary = Field() #工资水平: 如15k-25k
    positionAdvantage = Field() #氛围标签: 如下午茶
    industryField = Field() #公司营业领域: 如移动互联网
    financeStage = Field() #融资级别: 如成熟型(D轮及以上)
    companyLabelList = Field() #福利: 如节日礼物,绩效奖金
    district = Field() #县区
    companySize = Field() #公司规模: 如2000人及以上
    companyFullName = Field() #公司全名
    businessZones = Field() #附近定位: 如人民广场
    firstType = Field() #第一分类: 如技术
    secondType = Field() #第二分类: 如后端开发
    #用户信息,positionId
    userPositionName = Field() #职位: 如hr
    phone = Field()
    receiveEmail = Field()
    realName = Field() #真实姓名
    #detail
    detail = Field() #职位描述和要求
    address = Field() #详细地址
    website = Field() #官网
    #zhilian
    company_type = Field() #公司类型： 如国企，民营
    company_info = Field() #公司介绍
