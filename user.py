# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re


class HobbyStats(object):
    """
    书影音数据

    """

    def __init__(self, hobby, do=0, wish=0, collect=0):
        """
        初始化数据

        :param hobby: 喜好的类型：book, movie, music
        :param do: 对应正在的数量
        :param wish: 对应想要的数量
        :param collect: 对应做完的数量
        :type hobby: str
        :type do: int
        :type wish: int
        :type collect: int
        """
        super(HobbyStats, self).__init__()
        self.hobby = hobby
        self.do = do
        self.wish = wish
        self.collect = collect

    def print_stats(self):
        """
        打印喜好信息
        """
        print('喜好: {}\t do: {}\t wish: {}\t collect: {}'.format(self.hobby, self.do, self.wish, self.collect))


class DoubanUser(object):
    """
    豆瓣用户

    """

    def __init__(self, usr_id):
        """
        初始化普通豆瓣用户

        :param usr_id: 豆瓣ID
        :type usr_id: str
        """
        super(DoubanUser, self).__init__()
        self.usr_id = usr_id
        self.register_date = time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")
        self.com_likes = 0
        self.group_num = 0
        self.contacts_num = 0
        self.rev_contacts_num = 0
        self.stats_book = HobbyStats('book')
        self.stats_movie = HobbyStats('movie')
        self.stats_music = HobbyStats('music')
        self.usr_page_buffer = ''

    def set_register_date(self, register_date=time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")):
        """
        设置注册日期

        :param register_date: 注册日期
        :type register_date: time.struct_time
        """
        self.register_date = register_date

    def set_common_likes(self, com_likes=0):
        """
        设置共同喜好数目

        :param com_likes: 共同喜好数目
        :type com_likes: int
        """
        self.com_likes = com_likes

    def set_group_num(self, group_num=0):
        """
        设置关注的小组数目

        :param group_num: 关注的小组数目
        :type group_num: int
        """
        self.group_num = group_num

    def set_contacts_num(self, contacts_num=0):
        """
        设置关注的用户数目

        :param contacts_num: 关注的用户数目
        :type contacts_num: int
        """
        self.contacts_num = contacts_num

    def set_rev_contacts_num(self, rev_contacts_num=0):
        """
        设置被关注用户的数目

        :param rev_contacts_num: 被关注用户的数目
        :type rev_contacts_num: int
        """
        self.rev_contacts_num = rev_contacts_num

    def set_stats_book(self, stats):
        """
        设置书数据

        :param stats: 书数据
        :type stats: HobbyStats
        """
        self.stats_book = stats

    def set_stats_movie(self, stats):
        """
        设置影数据

        :param stats: 影数据
        :type stats: HobbyStats
        """
        self.stats_movie = stats

    def set_stats_music(self, stats):
        """
        设置音数据

        :param stats: 音数据
        :type stats: HobbyStats
        """
        self.stats_music = stats

    def set_cur_member_page(self, s):
        """
        获取当前成员的首页内容

        :param s: 一次连接会话
        :type s: requests.sessions.Session
        """
        usr_page_url = 'https://www.douban.com/people/{}'.format(self.usr_id)
        usr_page = s.get(usr_page_url)
        usr_page_buffer = usr_page.text
        self.usr_page_buffer = usr_page_buffer

    def get_register_date(self):
        """
        从当前成员的首页获得其加入的时间

        :return: 注册日期
        :rtype: time.struct_time
        """
        usr_page_buffer = self.usr_page_buffer
        register_date_str = re.search(r'(\d{4}-\d{1,2}-\d{1,2})加入', usr_page_buffer)
        if register_date_str and register_date_str is not '':
            return time.strptime(register_date_str.group(1), "%Y-%m-%d")
        return time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")

    def get_common_likes(self):
        """
        从当前成员的首页获得与对方的共同喜好数目

        :return: 共同喜好数目
        :rtype: int
        """
        usr_page_buffer = self.usr_page_buffer
        common_like_str = re.search(r'共同的喜好\((\d*)\)', usr_page_buffer)
        if common_like_str:
            return int(common_like_str.group(1))
        else:
            soup = BeautifulSoup(usr_page_buffer, features="lxml")
            win = soup.find('ul', {"id": "win"})
            if win:
                li = win.findAll('li', {"class": "aob"})
                if li:
                    return len(li)
        return 0

    def get_group_num(self):
        """
        从当前成员的首页获得其关注的小组数

        :return: 关注的小组数目
        :rtype: int
        """
        usr_page_buffer = self.usr_page_buffer
        group_num_str = re.search(r'常去的小组\((\d*)\)', usr_page_buffer)
        if group_num_str and group_num_str.group(1) is not '':
            return int(group_num_str.group(1))
        return 0

    def get_contacts_num(self):
        """
        从当前成员的首页获得其关注的用户数

        :return: 关注的用户数目
        :rtype: int
        """
        usr_page_buffer = self.usr_page_buffer
        contacts_num_str = re.search(r'成员(\d*)', usr_page_buffer)
        if contacts_num_str and contacts_num_str.group(1) is not '':
            return int(contacts_num_str.group(1))
        return 0

    def get_rev_contacts_num(self):
        """
        从当前成员的首页获得关注其的用户数

        :return: 被关注用户的数目
        :rtype: int
        """
        usr_page_buffer = self.usr_page_buffer
        rev_contacts_num_str = re.search(r'被(\d*)人关注', usr_page_buffer)
        if rev_contacts_num_str and rev_contacts_num_str.group(1) is not '':
            return int(rev_contacts_num_str.group(1))
        return 0

    def get_stats_book(self):
        """
        从当前成员的首页获得书的数据

        :return: 书数据
        :rtype: HobbyStats
        """
        usr_page_buffer = self.usr_page_buffer
        soup = BeautifulSoup(usr_page_buffer, features="lxml")
        div_book = soup.find('div', {'id': 'book'})
        do, wish, collect = 0, 0, 0
        if div_book:
            span_pl = div_book.find('span', {'class': 'pl'})
            if span_pl:
                do_str = re.search(r'(\d*)本在读', span_pl.text)
                if do_str and do_str.group(1) is not '':
                    do = int(do_str.group(1))
                wish_str = re.search(r'(\d*)本想读', span_pl.text)
                if wish_str and wish_str.group(1) is not '':
                    wish = int(wish_str.group(1))
                collect_str = re.search(r'(\d*)本读过', span_pl.text)
                if collect_str and collect_str.group(1) is not '':
                    collect = int(collect_str.group(1))
        return HobbyStats('book', do, wish, collect)

    def get_stats_movie(self):
        """
        从当前成员的首页获得影的数据

        :return: 影数据
        :rtype: HobbyStats
        """
        usr_page_buffer = self.usr_page_buffer
        soup = BeautifulSoup(usr_page_buffer, features="lxml")
        div_book = soup.find('div', {'id': 'movie'})
        do, wish, collect = 0, 0, 0
        if div_book:
            span_pl = div_book.find('span', {'class': 'pl'})
            if span_pl:
                do_str = re.search(r'(\d*)部在看', span_pl.text)
                if do_str and do_str.group(1) is not '':
                    do = int(do_str.group(1))
                wish_str = re.search(r'(\d*)部想看', span_pl.text)
                if wish_str and wish_str.group(1) is not '':
                    wish = int(wish_str.group(1))
                collect_str = re.search(r'(\d*)部看过', span_pl.text)
                if collect_str and collect_str.group(1) is not '':
                    collect = int(collect_str.group(1))
        return HobbyStats('movie', do, wish, collect)

    def get_stats_music(self):
        """
        从当前成员的首页获得音的数据

        :return: 音数据
        :rtype: HobbyStats
        """
        usr_page_buffer = self.usr_page_buffer
        soup = BeautifulSoup(usr_page_buffer, features="lxml")
        div_book = soup.find('div', {'id': 'music'})
        do, wish, collect = 0, 0, 0
        if div_book:
            span_pl = div_book.find('span', {'class': 'pl'})
            if span_pl:
                do_str = re.search(r'(\d*)张在听', span_pl.text)
                if do_str and do_str.group(1) is not '':
                    do = int(do_str.group(1))
                wish_str = re.search(r'(\d*)张想听', span_pl.text)
                if wish_str and wish_str.group(1) is not '':
                    wish = int(wish_str.group(1))
                collect_str = re.search(r'(\d*)张听过', span_pl.text)
                if collect_str and collect_str.group(1) is not '':
                    collect = int(collect_str.group(1))
        return HobbyStats('music', do, wish, collect)


class GroupMember(DoubanUser):
    """
    小组成员
    """

    def __init__(self, usr_id, usr_name, usr_addr, url_icon):
        """
        初始化基本信息

        :param usr_id: 豆瓣ID
        :param usr_name: 用户名
        :param usr_addr: 常居地地址
        :param url_icon: 头像url地址
        :type usr_id: str
        :type usr_name: str
        :type usr_addr: str
        :type url_icon: str
        """
        super(GroupMember, self).__init__(usr_id)
        self.usr_id = usr_id
        self.usr_name = usr_name
        self.usr_addr = usr_addr
        self.url_icon = url_icon

    def update_infos(self, data):
        """
        用于查询数据库时更新其它信息，方便打印

        :param data: 数据库查询得到的其它信息
        :type data: Tuple
        """
        # 注册日期
        if data[0] is None:
            self.register_date = time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d")
        else:
            self.register_date = time.strptime(data[0], "%Y-%m-%d")
        # 其它数据
        stats_num = lambda num: 0 if num is None else num
        self.com_likes = stats_num(data[1])
        self.group_num = stats_num(data[2])
        self.contacts_num = stats_num(data[3])
        self.rev_contacts_num = stats_num(data[4])
        # 书影音数据
        self.stats_book = HobbyStats('book', data[5], data[6], data[7])
        self.stats_movie = HobbyStats('movie', data[8], data[9], data[10])
        self.stats_music = HobbyStats('music', data[11], data[12], data[13])

    def print_basic_infos(self):
        """
        打印从小组成员页面可以获得的基本信息：昵称，常居地，用户ID(主页地址)，头像
        """
        # IMPROVE: 优雅的对齐输出
        usr_addr = (lambda addr: 'None' if addr is None else addr)(self.usr_addr)
        print('----------------------------------------------------------------------------------')
        print('主页: https://www.douban.com/people/{}'.format(self.usr_id))
        print('昵称: {:30s}\t 常居地: {:6s}'.format(self.usr_name, usr_addr))
        print('头像: {}'.format(self.url_icon))
        print('----------------------------------------------------------------------------------')

    def print_infos(self):
        """
        打印基本信息与通过访问用户的个人主页获得的剩余信息
        """
        self.print_basic_infos()
        print("加入: ", time.strftime("%Y-%m-%d", self.register_date))
        print('共同喜好数: {}\t 关注小组数: {}\t 关注用户数: {}\t 被关注用户数: {}'.format(
            self.com_likes, self.group_num, self.contacts_num, self.rev_contacts_num))
        self.stats_book.print_stats()
        self.stats_movie.print_stats()
        self.stats_music.print_stats()
        print('----------------------------------------------------------------------------------')
