import sqlite3
import psycopg2
from datetime import datetime


class PostgreConnector():
    def __init__(self):
        open('./postgre_errors.log', 'w').close()
        self.__con = psycopg2.connect(
            host='localhost', database='JOBMAA', user='postgres', password='docker')
        self.__cursor = self.__con.cursor()

    def close_connection(self):
        self.__cursor.close()
        self.__con.close()

    def run_query(self, item):
        try:
            self.__cursor.execute(f'''
                INSERT INTO
                    RAW_DATA ({', '.join([key for key in list(item.keys())])})
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING;
            ''', list(item.values()))
            self.__con.commit()
        except Exception as e:
            self.__con.rollback()
            with open('./postgre_errors.log', 'a') as file:
                file.write(f'{datetime.now()} --- {e} --- {item}')
                file.close()


class SQLiteConnector():
    def __init__(self):
        open('./sqlite3_errors.log', 'w').close()
        self.__con = sqlite3.connect('vagas_raw.db')
        self.__cursor = self.__con.cursor()
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS RAW_DATA(
                JOB_HASH CHAR(32) NOT NULL UNIQUE,
                SOURCE_ID VARCHAR(32) NOT NULL UNIQUE,
                HIERARCHY VARCHAR(64) NOT NULL,
                TITLE VARCHAR(256) NOT NULL,
                WAGE VARCHAR(32),
                LOCATION VARCHAR(32),
                DESCRIPTION TEXT NOT NULL,
                BENEFITS TEXT,
                URL TEXT NOT NULL,
                COMPANY_NAME VARCHAR(256) NOT NULL,
                COMPANY_INFO TEXT,
                PUBLISH_DATE DATE,
                EXTRACTION_TIMESTAMP TIMESTAMP NOT NULL,
                SOURCE VARCHAR(16) NOT NULL,
                PRIMARY KEY(JOB_HASH, SOURCE_ID)
            );
        ''')
        self.__con.commit()

    def close_connection(self):
        self.__cursor.close()
        self.__con.close()

    def run_query(self, item):
        try:
            self.__cursor.execute(f'''
                INSERT INTO
                    RAW_DATA ({', '.join([key for key in list(item.keys())])})
                VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT DO NOTHING;
            ''', self.__parse_item(item))
            self.__con.commit()
        except Exception as e:
            self.__con.rollback()
            with open('./sqlite3_errors.log', 'a') as file:
                file.write(f'{datetime.now()} --- {e} --- {item}')
                file.close()

    def __parse_item(self, item):
        parsed_values = []
        for value in list(item.values()):
            if(type(value) == list):
                parsed_values.append(','.join([v for v in value]))
            else:
                parsed_values.append(value)
        return parsed_values
