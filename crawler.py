# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import random
from urllib.request import urlretrieve
from PIL import Image

from config import config
from logger import log
from page_group import GroupList
from table_members import MembersTable
from table_proxy import ProxyTable


class Engine(object):
    def __init__(self):
        super(Engine, self).__init__()
        self.s = requests.Session()
        self.headers = None
        self.proxies = None
        self.set_headers()
        self.set_proxies()

    def login(self):
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
            r = self.s.post(url, data, headers=self.headers, proxies=self.proxies)
        print(config.get(option='cookie_tip'))
        print(json.dumps(self.s.cookies.get_dict(), sort_keys=True, indent =4, separators=(',', ': '), ensure_ascii=True))
    
    def set_headers(self):
        """设置请求头，随机的UA"""
        try:
            config.use_section('headers')
            self.headers = {
                config.get(option='connection_info'): config.get(option='connection'),
                config.get(option='user_agent_info'): config.get_ua()
            }
        except Exception as e:
            raise e

    def set_proxies(self):
        """设置代理IP"""
        p = ProxyTable()
        member = p.fetch_proxy_one()
        if member is None:
            raise LookupError
        else:
            self.proxies = {
                'http': 'http://' + member.ip_port
            }

    def run(self):
        """
        爬取数据，插入数据库中
        """
        try:
            # 登录
            self.login()
            # 小组成员页
            group_name = config.get('group','id')
            log.info(group_name)
            group = GroupList(self.s, group_name, self.headers, self.proxies)
            log.info('所爬小组：{}\t 总人数：{}\t 总页数{}'.format(group_name, group.total_members, group.total_pages))
            # 小组成员页获取错误
            if group.total_members is 0 or group.total_pages is 0:
                raise('所爬小组：{}\t 总人数：{}\t 总页数{}\n大概率账号被ban'.format(group_name, group.total_members, group.total_pages))

            # 设置开始爬的位置，倒着爬
            start_page = (lambda page_num: group.total_pages if page_num is -1 else page_num)(int(config.get('group', 'start_page')))
            end_page = (lambda page_num: 0 if page_num is -1 else page_num)(int(config.get('group', 'end_page')))
            # 开始按页爬小组成员页
            log.info('倒爬位置起始：{}\t 结束：{}'.format(start_page, end_page))

            # 数据库表
            members = MembersTable()
            # 删除表，新建表
            # members.drop_table()
            members.create()
            
            # TODO: 设置tqdm
            for page_num in range(start_page, end_page, -1):
                # IMPROVE: 设置新的头部和代理
                log.info('当前进度：[{}/{}]'.format(start_page-page_num,start_page-end_page))
                # 获取当前小组成员页的成员
                page_url = group.get_pageurl(page_num)
                page_members = group.get_contacts_from_pageurl(page_url)
                # 小组成员首页数据
                for member in page_members:
                    if members.is_existed_by_id(member.usr_id):
                        # 如果当前ID已经存在，则继续操作
                        print('用户：{} 已存在'.format(member.usr_id))
                        continue
                    member.set_cur_member_page(self.s)
                    # 获取注册日期
                    member.set_register_date(member.get_register_date())
                    # 获取共同喜好
                    member.set_common_likes(member.get_common_likes())
                    # 获取关注的小组数目，关注的用户数，被关注的用户数
                    member.set_group_num(member.get_group_num())
                    member.set_contacts_num(member.get_contacts_num())
                    member.set_rev_contacts_num(member.get_rev_contacts_num())
                    # 获取书影音的数据
                    member.set_stats_book(member.get_stats_book())
                    member.set_stats_movie(member.get_stats_movie())
                    member.set_stats_music(member.get_stats_music())
                    # 打印爬到的成员信息
                    # member.print_infos()
                    # 插入数据库
                    members.insert([member])
                    # 防止IP或者账号被ban的睡眠
                    time.sleep(random.randint(15,20))
                if start_page - page_num is 0:
                    log.info('爬到了第{}页'.format(page_num))
                    break
        except Exception as e:
            log.error(e)

    def crawl_group(self):
        # 小组成员页
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
                log.error(e)

    @staticmethod
    def crawl_group_members(start_page, end_page, group):
        try:
            # 开始按页爬小组成员页
            log.info('倒爬位置起始：{}\t 结束：{}'.format(start_page, end_page))
            members = MembersTable(table_name=config.get('group', 'id'))
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
                    time.sleep(random.randint(1,10))
        except Exception as e:
            raise e


if __name__ == '__main__':
    pass
