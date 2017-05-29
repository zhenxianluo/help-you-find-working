# -*- coding: utf-8 -*-

from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import psycopg2, logging

def exec_pgsql(sql):
    conn = psycopg2.connect(settings.get('PG_URL'))
    cur = conn.cursor()
    try:
        print sql
        cur.execute(sql)
        conn.commit()#进行提交操作，不提交则此次对数据库的更改无效
    except Exception, e:
        logging.error(sql)
    finally:
        cur.close()
        conn.close()

class WorksPipeline(object):
    def process_item(self, item, spider):
        keys = []
        values = []
        for key in item:
            keys.append(key)
            if isinstance(item[key], int):
                value = str(item[key])
            elif item[key] is None:
                value = ''
            else:
                value = item[key].encode('utf-8')
            values.append(value)
        insert_data = 'insert into works(%s) values(\'%s\');' % (','.join(keys), '\',\''.join(values))
        exec_pgsql(insert_data)
