# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import random
from urllib.request import urlretrieve
from PIL import Image

from config import Config
from logger import Logger
from group import GroupList
from table_members import MembersTable


class Engine(object):
    def __init__(self):
        super(Engine, self).__init__()
        self.c = Config()
        self.s = requests.Session()
    
    def login(self):
        """
        登录操作
        """
        self.c.use_section('login')
        url = self.c.get(option='url')
        self.c.use_section('login_data')
        data={
            'ck': self.c.get(option='ck'),
            'name': self.c.get(option='name'),
            'password': self.c.get(option='password'),
            'remember': self.c.get(option='remember'),
            'ticket': self.c.get(option='ticket'),
        }
        self.c.use_section('headers')
        headers = {
            self.c.get(option='user_agent_info'): self.c.get(option='user_agent')
        }
        r = self.s.post(url, data, headers=headers)
        html = r.json()
        self.c.use_section('info')
        # 判断是否登录成功
        if html['status'] == 'success':
            print(self.c.get(option='login_success'))
        else:
            print(self.c.get(option='login_failed'))
            print(self.c.get(option='captcha_image_path'),html['payload']['captcha_image_url'])
            # 获取加载验证码图片
            urlretrieve(html['payload']['captcha_image_url'],filename=self.c.get(option='captcha_image_name'))
            img = Image.open(self.c.get(option='captcha_image_name'))
            img.show()
            # 输入验证码信息
            captcha = input(self.c.get(option='captcha_tip'))
            print(captcha)
            data['captcha-solution'] = captcha
            data['captcha-id'] = html['payload']['captcha_id']
            # 再登录
            r = self.s.post(url, data, headers=headers)
        print(self.c.get(option='cookie_tip'))
        print(json.dumps(self.s.cookies.get_dict(), sort_keys=True, indent =4, separators=(',', ': '), ensure_ascii=True))
    
    def run(self):
        """
        爬取数据，插入数据库中
        """
        try:
            # 设置日志输出
            self.c.use_section('logger')
            sys.stdout = Logger(self.c.get(option='file_name'))
            # 登录
            self.login()
            # 小组成员页
            group_name = self.c.get('group','id')
            print(group_name)
            group = GroupList(self.s, group_name)
            print('所爬小组：{}\t 总人数：{}\t 总页数{}'.format(group_name, group.total_members, group.total_pages))
            # 小组成员页获取错误
            if group.total_members is 0 or group.total_pages is 0:
                raise('所爬小组：{}\t 总人数：{}\t 总页数{}\n大概率账号被ban'.format(group_name, group.total_members, group.total_pages))

            # 设置开始爬的位置，倒着爬
            start_page = (lambda page_num: group.total_pages if page_num is -1 else page_num)(int(self.c.get('group', 'start_page')))
            end_page = (lambda page_num: 0 if page_num is -1 else page_num)(int(self.c.get('group', 'end_page')))
            # 开始按页爬小组成员页
            print('倒爬位置起始：{}\t 结束：{}'.format(start_page, end_page))

            # 数据库表
            members = MembersTable()
            # 删除表，新建表
            # members.drop_table()
            members.create()
            
            # TODO: 设置tqdm
            for page_num in range(start_page, end_page, -1):
                print('当前进度：[{}/{}]'.format(start_page-page_num,start_page-end_page))
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
                    # member.printInfo()
                    # 插入数据库
                    members.insert([member])
                    # 防止IP或者账号被ban的睡眠
                    time.sleep(random.randint(15,20))
                if start_page - page_num is 1:
                    print('爬到了第{}页'.format(page_num))
                    break
        except Exception as e:
            print(e)
        

if __name__ == '__main__':
    Engine().run()
