# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import time
from config import Config
from user import GroupMember


class GroupList(object):
    """
    小组成员页相关操作
    """
    def __init__(self, session, group_id=''):
        """
        从小组拉取成员信息，小组成员页总页数
        """
        super(GroupList, self).__init__()
        self.s = session
        if group_id is '':
            group_id = Config().get('group', 'id')
        # 获取小组总人数
        self.group_members_url = "https://www.douban.com/group/{}/members".format(group_id)
        url_group_buffer = self.s.get(self.group_members_url).text
        bsObj = BeautifulSoup(url_group_buffer, features="lxml")
        span_count = bsObj.find('span', {'class': 'count'})
        total_members = 0
        if span_count:
            total_members_str = re.search(r'\(共(\d*)人\)', span_count.text)
            if total_members_str:
                total_members = int(total_members_str.group(1))
        self.total_members = total_members
        # 获取小组成员总页数
        paginator_div = bsObj.find('div', {'class': 'paginator'})
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
        # TODO: 过滤用户？
        # 无头像：https://img1.doubanio.com/icon/user_normal.jpg
        # 无地址
        # TODO: 爬不到页面应该raise error
        member_page = self.s.get(page_url)
        member_page_buffer = member_page.text
        soup = BeautifulSoup(member_page_buffer, features="lxml")
        div_list = soup.find('div', {'class': 'member-list'})
        if div_list is None:
            return []
        ul_user_list = div_list.findAll('li')
        member_list = []
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
        return member_list


if __name__ == '__main__':
    s = requests.Session()
    g = GroupList(s)
    for page_num in range(g.total_pages,0,-1):
        page_url = g.get_pageurl(page_num)
        page_members = g.get_contacts_from_pageurl(page_url)
        for member in page_members:
            member.print_basic_infos()
            time.sleep(2)
        break
