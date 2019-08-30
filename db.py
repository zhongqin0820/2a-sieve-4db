# -*- coding: utf-8 -*-
import sqlite3
import os
from config import Config


class DBHandler(object):
    """
    数据库相关的操作
    """
    def __init__(self, db_addr='', table_name=''):
        """
        设置默认数据库，默认操作表

        :param db_addr: 数据库文件
        :param table_name: 操作的表
        :type db_addr: str
        :type table_name: str
        """
        super(DBHandler, self).__init__()
        c = Config()
        config = c.items('database')
        self.type = config[0][1]
        self.default_db_addr = config[1][1]
        self.default_table_name = config[2][1]
        self.db_addr = (lambda name: self.default_db_addr if name is '' else name)(db_addr)
        self.table_name = (lambda name: self.default_table_name if name is '' else name)(table_name)
        self.conn = None
        self.cur = None

    def use_db(self, db_addr=''):
        """
        切换数据库，默认：group.db
        
        :param db_addr: 数据库文件
        :type db_addr: str
        """
        self.db_addr = (lambda name: self.default_db_addr if name is '' else name)(db_addr)

    def use_table(self, table_name=''):
        """
        切换表，默认：members

        :param table_name: 操作的表
        :type table_name: str
        """
        self.table_name = (lambda name: self.default_table_name if name is '' else name)(table_name)

    def set_conn(self):
        """
        建立数据库连接
        """
        db_addr = self.db_addr
        conn = sqlite3.connect(db_addr)
        if os.path.exists(db_addr) and os.path.isfile(db_addr):
            # 本地磁盘
            print('数据库类型:[{}], 位于磁盘:[{}]'.format(self.type, db_addr))
            self.conn = conn
        else:
            # 内存
            print('数据库类型:[{}], 位于内存:[{}]'.format(self.type, ':memory:'))
            self.conn = sqlite3.connect(':memory:')

    def set_cur(self):
        """
        游标相关操作：设置游标
        """
        if self.conn is None:
            self.set_conn()
            self.cur = self.conn.cursor()
        else:
            self.cur = self.conn.cursor()
    
    def get_cur(self):
        """
        游标相关操作：获取游标
        """
        self.set_cur()
        return self.cur

    def close_cur(self):
        """
        游标相关操作：关闭游标
        """
        try:
            if self.cur is not None:
                self.cur.close()
        finally:
            if self.cur is not None:
                self.cur.close()

    def drop_table(self):
        """
        如果表存在，删除表
        """
        table_name = self.table_name
        if table_name is not None and table_name is not '':
            sql = 'DROP TABLE IF EXISTS {}'.format(table_name)
            self.get_cur().execute(sql)
            self.conn.commit()
            self.close_cur()

    def fetch_all(self):
        """
        获取表内所有数据
        """
        try:
            table_name = self.table_name
            sql = 'SELECT * FROM {}'.format(table_name)
            members = self.get_cur().execute(sql).fetchall()
            self.conn.commit()
            self.close_cur()
            return members
        except Exception as e:
            print(e)
