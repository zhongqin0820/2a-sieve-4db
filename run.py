# -*- coding: utf-8 -*-
from crawler import Engine
from table_members import MembersTable
from table_proxy import ProxyTable
from config import config
from logger import log


def crawl_users():
    """从小组主页按页数倒爬用户首页信息"""
    e = Engine()
    e.run()


def crawl_group_members():
    """爬取小组成员页"""
    e = Engine()
    try:
        e.crawl_group()
    except Exception as e:
        log.error(e)


def print_table_info():
    """打印爬到小组的信息"""
    members = MembersTable(table_name=config.get('group', 'id'))
    items = members.fetch_all()
    num_before_insert = len(items)
    log.info('当前共有: {}'.format(num_before_insert))
    log.info('随机打印一个用户的信息')
    members.fetch_one_basic_infos().print_basic_infos()


def test_proxy():
    p = ProxyTable()
    # p.drop_table()
    # p.create()
    try:
        members = p.fetch_all()
    except Exception as e:
        log.error(e)
        log.info('当前代理池为空，重新开始爬代理信息')
        p.fetch_proxy()
    else:
        log.info('当前共有: {}'.format(len(members)))
    try:
        log.info('随机打印一个代理IP的信息')
        member = p.fetch_proxy_one()
    except Exception as e:
        log.error(e)
    else:
        member.print_infos()


if __name__ == '__main__':
    pass
    # TODO: 通过命令行的方式来切换逻辑
    # print_table_info()
    # test_proxy()
    crawl_group_members()
    # crawl_users()
