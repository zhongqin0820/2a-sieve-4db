# -*- coding: utf-8 -*-
import time
from db import DBHandler
from user import ContactsMember
from config import config


class ContactsTable(DBHandler):
    """
    与我的关注列表用户相关的CRUD操作
    """
    def __init__(self, db_addr='', table_name=''):
        c = config.items('database')
        table_name = (lambda name: c[4][1] if name is '' else table_name)(table_name)
        super(ContactsTable, self).__init__(db_addr, table_name)

    def create(self):
        """
        创建contacts表
        """
        try:
            sql = '''
            CREATE TABLE {} (
                `usr_id` varchar(15) NOT NULL,
                `usr_name` varchar(100) NOT NULL,
                `usr_addr` varchar(50) DEFAULT NULL,
                `url_icon` varchar(100) DEFAULT NULL,
                `usr_sign` varchar(100) DEFAULT NULL,
                `usr_rs` varchar(50) DEFAULT NULL,
                `register_date` date DEFAULT NULL,
                `com_likes` int(10) DEFAULT 0,
                `group_num` int(10) DEFAULT 0,
                `contacts_num` int(10) DEFAULT 0,
                `rev_contacts_num` int(10) DEFAULT 0,
                `stats_book_do` int(4) DEFAULT 0,
                `stats_book_wish` int(4) DEFAULT 0,
                `stats_book_collect` int(4) DEFAULT 0,
                `stats_movie_do` int(4) DEFAULT 0,
                `stats_movie_wish` int(4) DEFAULT 0,
                `stats_movie_collect` int(4) DEFAULT 0,                             
                `stats_music_do` int(4) DEFAULT 0,
                `stats_music_wish` int(4) DEFAULT 0,
                `stats_music_collect` int(4) DEFAULT 0,
                PRIMARY KEY (`usr_id`)
            )'''.format(self.get_table_name())
            self.get_cur().execute(sql)
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            raise e

    def insert_basic_infos(self, members):
        """
        插入成员的基本信息
        :param members: ContactsMember类型的实例列表
        :type members: List[ContactsMember]
        """
        try:
            table_name = self.get_table_name()
            sql = '''
            INSERT OR IGNORE INTO {} (usr_id, usr_name, usr_addr, url_icon, usr_sign, usr_rs) 
            VALUES (?,?,?,?,?,?)'''.format(table_name)
            for member in members:
                data = (
                    member.usr_id, 
                    member.usr_name, 
                    member.usr_addr, 
                    member.url_icon,
                    member.usr_sign,
                    member.usr_rs
                )
                self.get_cur().execute(sql, data)
                self.conn.commit()
            self.close_cur()
        except Exception as e:
            raise e

    def insert(self, members):
        """
        插入成员
        :param members: ContactsMember类型的实例列表
        :type members: List[ContactsMember]
        """
        try:
            table_name = self.get_table_name()
            sql = 'INSERT OR IGNORE INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(table_name)
            for member in members:
                data = self.deconv_member(member)
                self.get_cur().execute(sql, data)
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            raise e

    def delete(self, members):
        """
        按照usr_id删除成员
        :param members: ContactsMember类型的实例列表
        :type members: List[ContactsMember]
        """
        try:
            table_name = self.get_table_name()
            sql = 'DELETE FROM {} WHERE usr_id = ?'.format(table_name)
            for member in members:
                self.get_cur().execute(sql, [member.usr_id])
                self.conn.commit()
            self.close_cur()
        except Exception as e:
            raise e

    def fetch_one_basic_infos(self):
        """
        获取表内一个数据的基本信息
        :return: 包含基本信息的ContactsMember类实例
        :rtype: ContactsMember
        """
        try:
            table_name = self.get_table_name()
            sql = 'SELECT usr_id, usr_name, usr_addr, url_icon, usr_sign, usr_rs FROM {}'.format(table_name)
            member = self.get_cur().execute(sql).fetchone()
            self.conn.commit()
            self.close_cur()
            return ContactsMember(member[0], member[1], member[2], member[3], member[4], member[5])
        except Exception as e:
            raise e

    def is_existed_by_id(self, usr_id):
        """
        根据ID判断是否在表内

        :param usr_id: 用户ID
        :type usr_id: str
        :return: True表示存在，反之不存在
        :rtype: bool
        """
        try:
            table_name = self.get_table_name()
            sql = 'SELECT usr_id FROM {} WHERE usr_id = ?'.format(table_name)
            rowcount = len(self.get_cur().execute(sql,[usr_id]).fetchall())
            if rowcount >= 1:
                return True
            self.conn.commit()
            self.close_cur()
            return False
        except Exception as e:
            raise e

    def fecth_match_me(self):
        """
        过滤函数，找到匹配的用户
        """
        try:
            table_name = self.get_table_name()
            # 聚合分组操作
            sql = '''SELECT * FROM {}
            WHERE stats_book_collect >= 100
            '''.format(table_name)
            data = self.get_cur().execute(sql).fetchall()
            self.conn.commit()
            self.close_cur()
            return data
        except Exception as e:
            raise e

    @staticmethod
    def conv_member(data):
        """
        将查询到的数据恢复为ContactsMember类的实例

        :param data: 从表中查询到的数据，元祖类型
        :type data: Tuple
        :return: 转换后的ContactsMember类实例
        :rtype: ContactsMember
        """
        member = ContactsMember(data[0], data[1], data[2], data[3], data[4], data[5])
        member.update_infos(data[6:])
        return member

    @staticmethod
    def deconv_member(member):
        """
        将ContactsMember类的实例转换为插入元祖
        :param member: ContactsMember类实例
        :type member: ContactsMember
        :return: 转换后的元祖类型，用于插入数据库中
        :rtype: Tuple
        """
        data = (
            member.usr_id,  #usr_id
            member.usr_name,  #usr_name
            member.usr_addr,  #usr_addr
            member.url_icon,  #url_icon
            member.usr_sign,  #usr_sign
            member.usr_rs,  #usr_rs
            time.strftime("%Y-%m-%d", member.register_date),  #register_date
            member.com_likes,  #com_likes
            member.group_num,  #group_num
            member.contacts_num,  #contacts_num
            member.rev_contacts_num,  #rev_contacts_num
            member.stats_book.do,  #stats_book_do
            member.stats_book.wish,  #stats_book_wish
            member.stats_book.collect,  #stats_book_collect
            member.stats_movie.do,  #stats_movie_do
            member.stats_movie.wish,  #stats_movie_wish
            member.stats_movie.collect,  #stats_movie_collect
            member.stats_music.do,  #stats_music_do
            member.stats_music.wish,  #stats_music_wish
            member.stats_music.collect,  #stats_music_collect
        )
        return data


if __name__ == '__main__':
    pass
    # members = ContactsTable()
    # # members.create()
    # # 测试当前条目数
    # items = members.fetch_all()
    # num_before_insert = len(items)
    # print('当前共有: ', num_before_insert)
