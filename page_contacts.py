# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import time
from config import config
from user import ContactsMember
from crawler import Engine

class ContactsList(object):
    """
    关注列表页相关操作
    """
    def __init__(self, session):
        """
        从关注列表页拿到总的关注人数以及总的页数data-total-page
        """
        super(ContactsList, self).__init__()
        self.s = session
        self.contacts_page_url = 'https://www.douban.com/contacts/list?tag=0'
        self.page_buffer = self.s.get(self.contacts_page_url).text
        # 获取总的关注人数
        total_members_str = re.search(r'我关注的人\((\d*)\)', self.page_buffer)
        total_members = 0
        if total_members_str:
            total_members = int(total_members_str.group(1))
        self.total_members = total_members
        # 获取总的页数
        total_pages_str = re.search(r'data-total-page="(\d*)">', self.page_buffer)
        total_pages = 0
        if total_pages_str:
            total_pages = int(total_pages_str.group(1))
        self.total_pages = total_pages

    def get_page_url(self, page_num):
        """
        根绝页号拼接出关注列表页链接，其中tag=0是全部分组

        :param page_num: 关注列表页页号
        :type page_num: int
        :return: 关注列表页页号对应的url链接
        :rtype: str
        """
        # https://www.douban.com/contacts/list?tag=0&start=(page_num-1)*20
        return "{}&start={}".format(self.contacts_page_url, (page_num-1)*20)

    def set_page_buffer(self, page_num):
        page_url = self.get_page_url(page_num)
        self.page_buffer = self.s.get(page_url).text

    def get_contacts_from_page(self, page_num):
        if page_num > 1:
            self.set_page_buffer(page_num)
        soup = BeautifulSoup(self.page_buffer, features="lxml")
        ul_user_list = soup.find('div', {'class': 'article'})
        member_list = []
        if ul_user_list is None:
            return member_list
        ul_user_list = ul_user_list.findAll('li', {'class': 'clearfix'})
        if ul_user_list is None:
            return member_list
        for li in ul_user_list:
            if li is None:
                continue
            # 头像地址
            img = li.find('img')
            url_icon = img['src']
            div_info = li.find('div', {'class': 'info'})
            # IMPROVE: 此处真是神坑
            div_info_str = str(div_info)
            # ID
            usr_id_str = re.search(r'"https://www.douban.com/people/(.*)/"', div_info_str)
            usr_id = ''
            if usr_id_str:
                usr_id = usr_id_str.group(1)
            # 用户名
            usr_name = div_info.a['title']
            # 常居地
            # <span class="loc">常居：上海</span>
            usr_addr_str = re.search(r'<span class="loc">常居：(.*)</span>', div_info_str)
            usr_addr = ''
            if usr_addr_str:
                usr_addr = usr_addr_str.group(1)
            # 签名
            # <span class="signature">签名：XXXXXX</span>
            usr_sign_str = re.search(r'<span class="signature">签名：(.*)</span>', div_info_str)
            usr_sign = ''
            if usr_sign_str:
                usr_sign = usr_sign_str.group(1)
            # 分组信息
            # <span class="user-rs">未分组</span>
            usr_rs_str = re.search(r'<span class="user-rs">(.*)</span>', div_info_str)
            usr_rs = ''
            if usr_rs_str:
                usr_rs = usr_rs_str.group(1)

            m = ContactsMember(usr_id, usr_name, usr_addr, url_icon, usr_sign, usr_rs)
            member_list.append(m)
        return member_list

        
if __name__ == '__main__':
    pass
    # e = Engine()
    # e.login()
    # c = ContactsList(e.s)
    # total_members, total_pages = c.total_members, c.total_pages
    # print('共关注了{}位用户，列表页共有{}页'.format(c.total_members, c.total_pages))
    # for page_num in range(1, total_pages+1):
    #     print('当前进度：[{}/{}]'.format(page_num, total_pages))
    #     page_members = c.get_contacts_from_page(page_num)
    #     for member in page_members:
    #         member.print_basic_infos()
    #         time.sleep(5)
