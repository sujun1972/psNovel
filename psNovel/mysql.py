# -*- coding: utf-8 -*-
import pymysql.cursors


class MysqlNovelDB(object):
    def __init__(self, query):
        self.query = query
        self.connection = pymysql.connect(host='192.168.0.188',
                                         user='root',
                                         password='amxdjh8hj',
                                         db='novel',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def execute(self):
        try:
            self.cursor.execute(self.query)
            result = self.cursor.fetchall()
            self.connection.commit()
        except self.connection.Error as e:
            print(e)
            #print(self.query)
            self.connection.rollback()
            result = []
        finally:
            self.close()
        return result

    def close(self):
        self.connection.close()



if __name__ == "__main__":

    query = 'SELECT title From subjects'
    mysql = MysqlNovelDB(query)
    results = mysql.execute()
    for item in results:
        print(item)
