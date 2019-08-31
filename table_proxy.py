# -*- coding: utf-8 -*-
import time
from db import DBHandler
from page_proxy import ProxyItem, ProxyList
from logger import Logger
log = Logger().logger
import json
from config import Config


class ProxyTable(DBHandler):
    """
    与代理IP相关的CRUD操作
    """
    def __init__(self, db_addr='', table_name=Config().get('database', 'table_name_proxy')):
        super(ProxyTable, self).__init__(db_addr, table_name)

    def create(self):
        """
        创建代理IP表
        """
        try:
            sql = '''
            CREATE TABLE {} (
                `ip_port` varchar(24) NOT NULL,
                `create_date` date DEFAULT NULL,
                `is_valid` bool DEFAULT true,
                PRIMARY KEY (`ip_port`)
            )'''.format(self.get_table_name())
            self.get_cur().execute(sql)
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            log.error(e)

    def insert(self, members):
        """
        插入成员
        :param members: ProxyItem类型的实例列表
        :type members: List[ProxyItem]
        """
        try:
            table_name = self.get_table_name()
            sql = 'INSERT OR IGNORE INTO {} VALUES (?,?,?)'.format(table_name)
            for member in members:
                data = self.deconv_member(member)
                self.get_cur().execute(sql, data)
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            log.error(e)

    def delete(self, members):
        """
        按照ip_port删除成员
        """
        try:
            table_name = self.get_table_name()
            sql = 'DELETE FROM {} WHERE ip_port = ?'.format(table_name)
            for member in members:
                self.get_cur().execute(sql, [member.ip_port])
                self.conn.commit()
            self.close_cur()
        except Exception as e:
            log.error(e)

    def fetch_proxy(self):
        """
        获取表内一个数据的基本信息

        :return: 包含基本信息的ProxyItem类实例
        :rtype: ProxyItem
        """
        try:
            table_name = self.get_table_name()
            sql = 'SELECT * FROM {} WHERE is_valid = 1 ORDER BY RANDOM() LIMIT 1'.format(table_name)
            member = self.get_cur().execute(sql).fetchone()
            if member is None:
                # 重新拉数据，插入数据，重新查询
                members = ProxyList().crawl()
                self.insert(members)
                self.fetch_proxy()
            else:
                member = self.conv_member(member)
                if not member.valid_proxy():
                    # 删除该数据，重新查询
                    self.delete([member])
                    self.fetch_proxy()
                else:
                    return member
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            log.error(e)
            return None

    def fetch_proxy_one(self):
        """
        获取表内一个数据的基本信息

        :return: 包含基本信息的ProxyItem类实例
        :rtype: ProxyItem
        """
        try:
            table_name = self.get_table_name()
            sql = 'SELECT * FROM {} WHERE is_valid = 1 ORDER BY RANDOM() LIMIT 1'.format(table_name)
            member = self.get_cur().execute(sql).fetchone()
            member = self.conv_member(member)
            self.conn.commit()
            self.close_cur()
            return member
        except Exception as e:
            log.error(e)
            return None

    @staticmethod
    def conv_member(data):
        """
        将查询到的数据恢复为ProxyItem类的实例

        :param data: 从表中查询到的数据，元祖类型
        :type data: Tuple
        :return: 转换后的ProxyItem类实例
        :rtype: ProxyItem
        """
        member = ProxyItem(data[0], time.strptime(data[1], "%Y-%m-%d"), data[2])
        return member

    @staticmethod
    def deconv_member(member):
        """
        将ProxyItem类的实例转换为插入元祖

        :param member: ProxyItem类实例
        :type member: ProxyItem
        :return: 转换后的元祖类型，用于插入数据库中
        :rtype: Tuple
        """
        data = (
            member.ip_port,  #ip_port
            time.strftime("%Y-%m-%d", member.create_date),  #create_date
            member.is_valid,  #is_valid
        )
        return data


if __name__ == '__main__':
    p = ProxyTable()
    # p.create()
    members = p.fetch_all()
    print(len(members))
    # member = p.fetch_proxy()
    member = p.fetch_proxy_one()
    member.print_infos()
    # file_name = 'proxy.json'
    # with open(file_name, 'r') as f:
    #     proxies = json.load(f)
    #     for proxy in proxies:
    #         member = p.conv_member([proxy['ip_port'], proxy['create_date'], proxy['is_valid']])
    #         p.insert([member])
    # p.fetch_proxy().print_infos()
