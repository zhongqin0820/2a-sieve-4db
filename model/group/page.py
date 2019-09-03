# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import time
from common.config import config
from common.logger import log
from ..common.user import GroupMember
from ..proxy.table import ProxyTable


class GroupList(object):
    """
    小组成员页相关操作
    """
    def __init__(self, session=requests.Session(), group_id='', headers=None, proxies=None):
        """
        从小组拉取成员信息，小组成员页总页数
        """
        super(GroupList, self).__init__()
        # 设置默认的参数
        self.s = session
        if group_id is '':
            group_id = config.get('group', 'id')
        if headers is None:
            self.set_headers()
        else:
            self.headers = headers
        if proxies is None:
            self.set_proxies()
        else:
            self.proxies = proxies
        # 获取小组总人数
        self.group_members_url = "https://www.douban.com/group/{}/members".format(group_id)
        try:
            # 建立连接
            r = self.s.get(self.group_members_url, headers=self.headers, proxies=self.proxies, allow_redirects=False, timeout=20)
            if r.status_code != 200:
                # 连接失败
                raise Exception('status: {}, url: {}'.format(r.status_code, r.url))
        except Exception as e:
            raise Exception('GroupList: {}'.format(e))
        else:
            url_group_buffer = r.text
            # IMPROVE: 需要在BeautifulSoup和re中择一进行解析
            soup = BeautifulSoup(url_group_buffer, features="lxml")
            span_count = soup.find('span', {'class': 'count'})
            total_members = 0
            # 获取小组成员总数
            if span_count:
                total_members_str = re.search(r'\(共(\d*)人\)', span_count.text)
                if total_members_str:
                    total_members = int(total_members_str.group(1))
            self.total_members = total_members
            # 获取小组成员总页数
            paginator_div = soup.find('div', {'class': 'paginator'})
            total_pages = 0
            if paginator_div:
                total_pages_str = paginator_div.findAll('a')[-2].string
                if total_pages_str:
                    total_pages = int(total_pages_str)
            self.total_pages = total_pages
 
    def get_pageurl(self, page_num):
        """
        根绝页号拼接出小组成员列表页链接

        :param page_num: 小组成员页页号
        :type page_num: int
        :return: 小组成员页页号对应的url链接
        :rtype: str
        """
        # https://www.douban.com/group/group_id/members?start=(page_num-1)*35
        return "{}?start={}".format(self.group_members_url,(page_num-1)*35)

    def get_contacts_from_pageurl(self, page_url):
        """
        从小组成员列表页获取该页所有成员的基本信息

        :param page_url: 小组成员页页号对应的url链接
        :type page_url: str
        :return: 当前页不在数据库内的成员列表
        :rtype: List[GroupMember]
        """
        member_page = self.s.get(page_url, headers=self.headers, proxies=self.proxies, allow_redirects=False, timeout=20)
        member_page_buffer = member_page.text
        soup = BeautifulSoup(member_page_buffer, features="lxml")
        div_list = soup.find('div', {'class': 'member-list'})
        if div_list is None:
            raise Exception('div_list is None')
        ul_user_list = div_list.findAll('li')
        member_list = []
        # 提取信息
        if ul_user_list:
            for li in ul_user_list:
                if li:
                    # icon, id, name
                    div_pic = li.find('div', {'class': 'pic'})
                    if div_pic:
                        usr_id = re.search(r'https://www.douban.com/people/(.*)/', div_pic.a['href']).group(1)
                        usr_name = div_pic.a.img['alt']
                        url_icon = div_pic.a.img['src']
                        # places
                        div_name = li.find('div', {'class': 'name'})
                        usr_addr = ''
                        if div_name:
                            span_pl = div_name.find('span', {'class':'pl'})
                            if span_pl:
                                usr_addr = re.search(r'\((.*)\)', span_pl.text)
                                if usr_addr:
                                    usr_addr = usr_addr.group(1)
                        m = GroupMember(usr_id,usr_name,usr_addr,url_icon)
                        member_list.append(m)
                    else:
                        raise Exception('div_pic is None')
                else:
                    raise Exception('li is None')
        else:
            raise Exception('ul_user_list is None')
        return member_list

    def set_headers(self):
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
        p = ProxyTable()
        member = p.fetch_proxy()
        if member is None:
            raise Exception('set_proxies: {}'.format('member is None'))
        else:
            self.proxies = {
                'http': 'http://' + member.ip_port
            }
            log.info('{}'.format(self.proxies))
