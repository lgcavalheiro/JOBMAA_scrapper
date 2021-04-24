# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
from datetime import datetime
import psycopg2


class ScrappersPipeline:
    def process_item(self, item, spider):
        return item


class PostgresPipeline(object):
    def open_spider(self, spider):
        self.con = psycopg2.connect(
            host='localhost', database='JOBMAA', user='postgres', password='docker')
        self.cursor = self.con.cursor()
        open('./postgre_errors.log', 'w').close()

    def close_spider(self, spider):
        self.con.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(f'''
                INSERT INTO 
                    RAW_DATA ({', '.join([key for key in list(item.keys())])})
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING;
            ''', list(item.values()))
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            with open('./postgre_errors.log', 'a') as file:
                file.write(f'{datetime.now()} --- {e} --- {item}')
                file.close()

        return item
