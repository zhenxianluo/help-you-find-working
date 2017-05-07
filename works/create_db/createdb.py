# coding:utf-8
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import psycopg2

def exec_pgsql(sql):
    conn = psycopg2.connect(settings.get('PG_URL'))
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()#进行提交操作，不提交则此次对数据库的更改无效
    finally:
        cur.close()
        conn.close()

createdb = ''' 
create table works(
    id serial primary key,
    origin text,
    positionName text,
    workYear text,
    education text,
    jobNature text,
    createTime timestamp,
    companyShortName text,
    city text,
    salary text,
    positionAdvantage text,
    industryField text,
    financeStage text,
    companyLabelList text,
    district text,
    companySize text,
    companyFullName text,
    businessZones text,
    firstType text,
    secondType text,
    userPositionName text,
    phone text,
    receiveEmail text,
    realName text,
    detail text,
    address text,
    website text,
    company_type text,
    company_info text
);
'''
if __name__ == '__main__':
    exec_pgsql(createdb)
