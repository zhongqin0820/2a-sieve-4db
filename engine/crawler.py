# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import random
from urllib.request import urlretrieve
from PIL import Image

from common.config import config
from common.logger import log
from model.group.page import GroupList
from model.group.table import MembersTable
from model.contacts.page import ContactsList
from model.contacts.table import ContactsTable
from model.proxy.table import ProxyTable


class Engine(object):
    def __init__(self):
        super(Engine, self).__init__()
        self.s = requests.Session()
        self.headers = None
        self.proxies = None
        self.set_proxies()
        self.set_headers()
    
    def set_headers(self):
        """设置请求头，随机的UA"""
        try:
            config.use_section('headers')
            self.headers = {
                config.get(option='connection_info'): config.get(option='connection'),
                config.get(option='user_agent_info'): config.get_ua()
            }
            log.info('{}'.format(self.headers))
        except Exception as e:
            raise Exception('set_headers: {}'.format(e))

    def set_proxies(self):
        """设置代理IP"""
        p = ProxyTable()
        member = p.fetch_proxy_one()
        if member is None:
            raise Exception('set_proxies: {}'.format('member is None'))
        else:
            self.proxies = {
                'http': 'http://' + member.ip_port
            }
            log.info('{}'.format(self.proxies))

    def login(self, data=dict()):
        """
        登录操作
        """
        config.use_section('login')
        url = config.get(option='url')
        config.use_section('login_data')
        data={
            'ck': config.get(option='ck'),
            'name': config.get(option='name'),
            'password': config.get(option='password'),
            'remember': config.get(option='remember'),
            'ticket': config.get(option='ticket'),
        }
        # 登录
        r = self.s.post(url, data, headers=self.headers, proxies=self.proxies)
        html = r.json()
        config.use_section('info')
        # 判断是否登录成功
        if html['status'] == 'success':
            print(config.get(option='login_success'))
        else:
            print(config.get(option='login_failed'))
            print(config.get(option='captcha_image_path'),html['payload']['captcha_image_url'])
            # 获取加载验证码图片
            urlretrieve(html['payload']['captcha_image_url'],filename=config.get(option='captcha_image_name'))
            img = Image.open(config.get(option='captcha_image_name'))
            img.show()
            # 输入验证码信息
            captcha = input(config.get(option='captcha_tip'))
            print(captcha)
            data['captcha-solution'] = captcha
            data['captcha-id'] = html['payload']['captcha_id']
            # 再登录
            self.login(data)
            # r = self.s.post(url, data, headers=self.headers, proxies=self.proxies)
        print(config.get(option='cookie_tip'))
        print(json.dumps(self.s.cookies.get_dict(), sort_keys=True, indent =4, separators=(',', ': '), ensure_ascii=True))

    def crawl_contacts(self):
        """爬小组用户的关注列表页并写入数据库中对应用户名的表中"""
        try:
            self.login()
            # 关注用户表，表名对应当前用户id
            user_id = config.get('user', 'id')
            contacts = ContactsTable(table_name=user_id)
            c = ContactsList(self.s)
            total_members, total_pages = c.total_members, c.total_pages
            log.info('共关注了{}位用户，列表页共有{}页'.format(c.total_members, c.total_pages))
            # 
            for page_num in range(1, total_pages+1):
                log.info('当前进度：[{}/{}]'.format(page_num, total_pages))
                try:
                    page_members = c.get_contacts_from_page(page_num)
                except Exception as e:
                    raise Exception('因为{}, 无法爬取页：{} 至 {}'.format(e, page_num, total_pages))
                else:
                    contacts.insert(page_members)
                    # 防止IP或者账号被ban的睡眠
                    time.sleep(random.randint(3,20))
        except Exception as e:
            raise Exception('crawl_contacts: {}'.format(e))

    def crawl_group(self):
        """爬小组成员页"""
        group_name = config.get('group', 'id')
        log.info(group_name)
        group = GroupList()
        if group.total_members is 0 or group.total_pages is 0:
            # 小组成员页获取错误
            raise Exception('所爬小组：{}\t 总人数：{}\t 总页数{}\n大概率账号被ban'.format(group_name, group.total_members, group.total_pages))
        else:
            log.info('所爬小组：{}\t 总人数：{}\t 总页数{}'.format(group_name, group.total_members, group.total_pages))
        # 设置开始爬的位置，倒着爬
        start_page = (lambda page_num: group.total_pages if page_num is -1 else page_num)(int(config.get('group', 'start_page')))
        end_page = (lambda page_num: 0 if page_num is -1 else page_num)(int(config.get('group', 'end_page')))

        # 开始爬，每倒爬step页换一个headers和proxies
        step = int(config.get('group', 'skip_page'))
        for page_range in range(start_page, end_page, step):
            # 换一个headers和proxies
            group = GroupList()
            try:
                self.crawl_group_members(page_range, page_range+step, group)
            except Exception as e:
                raise Exception('crawl_group: {}'.format(e))

    @staticmethod
    def crawl_group_members(start_page, end_page, group):
        try:
            # 开始按页爬小组成员页
            log.info('倒爬位置起始：{}\t 结束：{}'.format(start_page, end_page))
            for page_num in range(start_page, end_page, -1):
                log.info('当前进度：[{}/{}]'.format(start_page-page_num, start_page-end_page))
                # 获取当前小组成员页的成员
                page_url = group.get_pageurl(page_num)
                try:
                    page_members = group.get_contacts_from_pageurl(page_url)
                except Exception as e:
                    raise Exception('因为{}, 无法爬取页：{} 至 {}'.format(e, page_num, end_page))
                else:
                    members.insert(page_members)
                    # 防止IP或者账号被ban的睡眠
                    time.sleep(random.randint(3,20))
        except Exception as e:
            raise Exception('crawl_group_members: {}'.format(e))

    def crawl_group_member(self):
        """
        爬取小组成员首页数据，更新插入数据库表members中，并将更新后的用户从小组对应的表中删除
        """
        try:
            # 登录
            self.login()
            # 用户表：存储已经更新完数据，具有完整首页数据字段
            users = MembersTable()
            # 小组成员表：数据是待更新首页信息的小组成员：只包含基本信息
            group_id = config.get('group','id')
            group = MembersTable(table_name=group_id)
            # 从数据库拉取没有对应首页字段内容的用户，迭代爬取首页内容，更新字段
            while True:
                # 从小组表中随机拉取一个成员
                user = group.fetch_one_not_updated()
                if users.is_existed_by_id(user.usr_id):
                    # 如果当前ID已经存在，则继续操作
                    print('用户：{} 已存在'.format(user.usr_id))
                    continue
                # 小组成员首页数据获取
                # IMPROVE: 每次self.s.get()的时候重新设置新的头部和代理
                user.set_cur_member_page(self.s)
                # 更新数据信息：注册日期
                user.set_register_date(user.get_register_date())
                # 更新数据信息：共同喜好
                user.set_common_likes(user.get_common_likes())
                # 更新数据信息：关注的小组数目，关注的用户数，被关注的用户数
                user.set_group_num(user.get_group_num())
                user.set_contacts_num(user.get_contacts_num())
                user.set_rev_contacts_num(user.get_rev_contacts_num())
                # 更新数据信息：书影音的数据
                user.set_stats_book(user.get_stats_book())
                user.set_stats_movie(user.get_stats_movie())
                user.set_stats_music(user.get_stats_music())
                # 打印爬到的成员信息
                # user.print_infos()
                # 将更新完信息的user插入用户表中
                users.insert([user])
                # 从小组成员表中删除该成员user
                group.delete([user])
                # 防止IP或者账号被ban的睡眠
                time.sleep(random.randint(15,20))
        except Exception as e:
            raise Exception('crawl_home_page: {}'.format(e))
