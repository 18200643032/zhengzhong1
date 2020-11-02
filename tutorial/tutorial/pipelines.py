# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymysql

class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self,item,spider):

        if item["text"]:
            if len(item["text"]) >self.limit:
                item["text"] = item["text"][0:self.limit].rstrip() + '....'
                return item
        else:
            return DropItem("Missing Text")


class MysqlPipeline():
    def __init__(self,host,database,user,password,port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            database = crawler.settings.get("MYSQL_DATABASE"),
            user = crawler.settings.get("MYSQL_USER"),
            password = crawler.settings.get("MYSQL_PASSWORD"),
            port = crawler.settings.get("MYSQL_PORT"),
            )

    def open_spider(self,spider):
        self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset='utf8',port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self,spider):
        self.db.close()

    def process_item(self,item,spider):
        # print(item['title'])
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)'%(item.table,keys,values)
        print(sql)
        print("===")
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item