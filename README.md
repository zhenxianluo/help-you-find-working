# 基于scrapy的爬虫

爬虫实现的功能：爬取智联招聘及拉勾网的关于Python及上海的招聘信息。

实现语言：`Python`  
爬虫框架：`scrapy`  
数据库：`PostgreSQL`

Python、PostgreSQL及scrapy都搭好后执行如下步骤：

1. 克隆本git仓库：`git clone git@github.com:zhenxianluo/help-you-find-working.git`
2. 进入项目目录：`cd help-you-find-work`
3. 安装依赖包：`pip install -r requirement.txt`
4. 修改pgsql的uri连接串：打开文件‘vim works/settings.py’可以看到最后一行是配置连接pgsql的，改成你自己的用户及密码。
5. 新建works表用来存储数据：`python works/create_db/createdb.py`
6. 执行爬虫：`scrapy crawl lagou`和`scrapy crawl zhilian`
7. 进入数据库将数据导出到csv：`\COPY dbname TO '/tmp/data.csv' DELIMITER ';' CSV HEADER`
8. 执行csv转xlsx转换脚本：`python csv2xlsx.py`(可指定csv文件的字段分隔符及转换路径)

文件lagou.xlsx为最终数据结果。

交流联系：<chinaitlearner@foxmail.com>或<zxl_d@foxmail.com>

本人博客：[http://howduudu.xyz](http://howduudu.xyz) 或 https://zhenxianluo.github.com
