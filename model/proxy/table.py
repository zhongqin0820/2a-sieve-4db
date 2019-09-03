# -*- coding: utf-8 -*-
import time
import json
from common.db import DBHandler
from common.config import config
from common.logger import log
from .page import ProxyItem, ProxyList


class ProxyTable(DBHandler):
    """
    与代理IP相关的CRUD操作
    """
    def __init__(self, db_addr='', table_name=config.get('database', 'table_name_proxy')):
        super(ProxyTable, self).__init__(db_addr, table_name)
        self.create()

    def create(self):
        """
        创建代理IP表
        """
        try:
            sql = '''
            CREATE TABLE IF NOT EXISTS {} (
                `ip_port` varchar(24) NOT NULL,
                `create_date` date DEFAULT NULL,
                `is_valid` bool DEFAULT FALSE,
                PRIMARY KEY (`ip_port`)
            )'''.format(self.get_table_name())
            self.get_cur().execute(sql)
        except Exception as e:
            raise Exception('create: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

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
        except Exception as e:
            raise Exception('insert: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def delete(self, members):
        """
        按照ip_port删除成员
        """
        try:
            table_name = self.get_table_name()
            sql = 'DELETE FROM {} WHERE ip_port = ?'.format(table_name)
            for member in members:
                self.get_cur().execute(sql, [member.ip_port])
        except Exception as e:
            raise Exception('delete: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def fetch_proxy(self):
        """
        获取表内一个数据的基本信息

        :return: 包含基本信息的ProxyItem类实例
        :rtype: ProxyItem
        """
        try:
            num = len(self.fetch_all())
            log.info('查询，当前共有: {}'.format(num))
            if num == 0:
                # 重新拉数据，插入数据，重新查询
                log.info('重新拉数据')
                try:
                    members = ProxyList().crawl()
                except Exception as e:
                    raise e
                else:
                    log.info('插入新数据: {}条'.format(len(members)))
                    self.insert(members)
                    return self.fetch_proxy()
            else:
                return self.fetch_proxy_one()
        except Exception as e:
            raise Exception('fetch_proxy: {}'.format(e))

    def fetch_proxy_one(self):
        """
        获取表内一个数据的基本信息

        :return: 包含基本信息的ProxyItem类实例
        :rtype: ProxyItem
        """
        try:
            table_name = self.get_table_name()
            sql = 'SELECT * FROM {} WHERE is_valid = TRUE ORDER BY RANDOM() LIMIT 1'.format(table_name)
            member = self.get_cur().execute(sql).fetchone()
            member = self.conv_member(member)
            return member
        except Exception as e:
            raise Exception('fetch_proxy_one: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

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
