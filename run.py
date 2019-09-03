# -*- coding: utf-8 -*-
import sys
from common.config import config
from common.logger import log
from common.db import DBHandler
from model.proxy.table import ProxyTable
from model.proxy.page import ProxyList
from model.group.table import MembersTable
from model.contacts.table import ContactsTable
from engine.crawler import Engine


class Switcher(object):
    def __init__(self, option=1):
        super(Switcher, self).__init__()
        self.option = option

    def set_option(self, option=1):
        if option == 0:
            return
        self.option = option

    def switch(self, option=0):
        if option == 0:
            self.switch(self.option)
        elif option == 1:
            self.test_config()
        elif option == 2:
            self.test_log()
        elif option == 3:
            self.test_proxy()
        elif option == 4:
            self.print_proxy_table()
        elif option == 5:
            self.test_login()
        elif option == 6:
            self.test_crawl_contacts()
        elif option == 7:
            self.test_crawl_group()
        elif option == 8:
            self.test_crawl_group_member()
        elif option == 9:
            self.test_db()
        elif option == 10:
            self.print_group_table()
        elif option == 11:
            self.print_contacts_table()
        elif option == 12:
            self.print_group_match_me()
        else:
            log.warning('option not implemented!')

    # 测试config和logger
    def test_config(self):
        print(config.get('database', 'type'))

    def test_log(self):
        log.info('!!!info!!!')

    # 与代理IP相关
    def test_proxy(self):
        """测试代理IP拉取"""
        ProxyList().test()

    def print_proxy_table(self):
        """随机打印一个代理IP的信息"""
        p = ProxyTable()
        try:
            log.info('随机打印一个代理IP的信息')
            member = p.fetch_proxy()
        except Exception as e:
            log.error(e)
        else:
            member.print_infos()

    # Engine相关操作
    def test_login(self):
        """测试登录操作"""
        e = Engine()
        e.login()

    def test_crawl_contacts(self):
        """拉取关注列表页数据"""
        e = Engine()
        e.crawl_contacts()

    def test_crawl_group(self):
        """拉取小组成员页数据"""
        e = Engine()
        e.crawl_group()

    def test_crawl_group_member(self):
        """从小组成员表中更新数据到用户表中"""
        e = Engine()
        e.crawl_group_member()

    # 数据库查询相关操作
    def test_db(self):
        """测试数据库连接"""
        db = DBHandler()
        print(db.get_table_name())
        print(len(db.fetch_all()))

    def print_group_table(self):
        """打印拉取到的小组成员页数据"""
        members = MembersTable(table_name=config.get('group', 'id'))
        items = members.fetch_all()
        num_existed = len(items)
        log.info('当前共有: {}'.format(num_existed))
        log.info('随机打印一个用户的信息')
        members.fetch_one_basic_infos().print_basic_infos()

    def print_contacts_table(self):
        """打印拉取到的关注列表页数据"""
        members = ContactsTable()
        items = members.fetch_all()
        num_existed = len(items)
        log.info('当前共有: {}'.format(num_existed))
        log.info('随机打印一个用户的信息')
        members.fetch_one_basic_infos().print_basic_infos()

    def print_group_match_me(self):
        """随机打印一个打印从成员表中过滤得到的用户"""
        members = MembersTable(table_name=config.get('database', 'table_name_members'))
        items = members.fecth_all_match_me()
        print('----------------------------------------------------------------------------------')
        print('过滤得到的用户数: ', len(items))
        for item in items:
            member = members.conv_member(item)
            member.print_infos()
            # member.print_basic_infos()
            print()
            break


def run(option):
    Switcher(option).switch()


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 2 or len(args) == 1:
        print("""
        Usage:
            python run.py <option>
        Options:
            1 - 测试config
            2 - 测试logger
            3~4 - 与代理IP相关
                3 - 测试代理IP拉取
                4 - 随机打印一个代理IP的信息
            5~8 - Engine相关操作
                5 - 测试登录操作
                6 - 拉取关注列表页数据
                7 - 拉取小组成员页数据
                8 - 从小组成员表中更新数据到用户表中
            9~12 - 数据库查询相关操作
                9 - 测试数据库连接
                10 - 打印拉取到的小组成员页数据
                11 - 打印拉取到的关注列表页数据
                12 - 随机打印一个打印从成员表中过滤得到的用户
        """)
    else:
        option = int(args[1])
        run(option)
