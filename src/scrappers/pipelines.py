# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from .utils.db_utils import SQLiteConnector, PostgreConnector
from datetime import datetime

DB_literals = {
    'POSTGRE': PostgreConnector,
    'SQLITE': SQLiteConnector
}


class DatabasePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        try:
            DBCON = crawler.settings.attributes.get('DBCON').value
            LOG_FILE = crawler.settings.attributes.get('LOG_FILE').value
        except Exception as e:
            print(f'ERROR WHILE EXTRACTING SETTINGS: {e}')
            DBCON = 'SQLITE'
            LOG_FILE = 'error.log'
        return cls(LOG_FILE, DBCON)

    def __init__(self, LOG_FILE, DBCON):
        self.__connector_class = DB_literals[DBCON]
        open(LOG_FILE, 'w').close()

    def open_spider(self, spider):
        self.__connector = self.__connector_class()

    def close_spider(self, spider):
        self.__connector.close_connection()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        hasError = False
        for val in adapter.values():
            if('DATA PROCESS ERROR' in str(val)):
                hasError = True
                msg = f"Data process error found @ {adapter['SOURCE_ID']}-{adapter['JOB_HASH']}"
                print(msg)
                raise DropItem(msg)
        if(not hasError):
            self.__connector.run_query(item)
            return item
