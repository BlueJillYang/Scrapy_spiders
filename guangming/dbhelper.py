# -*- coding: utf-8 -*-

from settings import MYSQL_PARAMS
import MySQLdb


class Dbhelper(object):
    def __init__(self):
        self.host = MYSQL_PARAMS['host']
        self.user = MYSQL_PARAMS['user']
        self.port = MYSQL_PARAMS['port']
        self.passwd = MYSQL_PARAMS['password']
        self.db = MYSQL_PARAMS['db']

    def connenct_mysql(self):
        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.passwd,
                               port=self.port,
                               charset='utf8')
        return conn

    def connenct_db(self):
        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.passwd,
                               port=self.port,
                               db=self.db, charset='utf8')
        return conn

    def create_database(self):
        conn = self.connenct_mysql()
        cur = conn.cursor()
        sql = 'create database if not exists {}'.format(self.db)
        try:
            cur.execute(sql)
            conn.commit()
        except Exception:
            print 'create_database失败 回溯'
            conn.rollback()
        cur.close()
        conn.close()

    def create_table(self, sql):
        conn = self.connenct_db()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception:
            print 'create_table失败 回溯'
            conn.rollback()
        cur.close()
        conn.close()

    def insert(self, sql):
        conn = self.connenct_db()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception:
            print 'insert失败 回溯'
            conn.rollback()
        cur.close()
        conn.close()


if __name__ == '__main__':
    dbhelper = Dbhelper()
    dbhelper.connenct_mysql()
    dbhelper.connenct_db()
    # sql = 'create table test1(id int primary key auto_increment,name varchar(20));'
    # dbhelper.create_table(sql)
    dbhelper.insert('insert into test1(name) value(\'testname1\') ')

