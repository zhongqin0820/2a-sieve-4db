# -*- coding: utf-8 -*-
import time
from common.config import config
from common.db import DBHandler
from ..common.user import GroupMember


class MembersTable(DBHandler):
    """
    与小组成员表相关的CRUD操作
    """
    def __init__(self, db_addr='', table_name=config.get('database', 'table_name_members')):
        super(MembersTable, self).__init__(db_addr, table_name)
        self.create()

    def create(self):
        """
        创建小组成员表
        """
        try:
            sql = '''
            CREATE TABLE IF NOT EXISTS {} (
                `usr_id` varchar(15) NOT NULL,
                `usr_name` varchar(100) NOT NULL,
                `usr_addr` varchar(50) DEFAULT NULL,
                `url_icon` varchar(100) DEFAULT NULL,
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
        except Exception as e:
            raise Exception('create: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def insert_basic_infos(self, members):
        """
        插入成员的基本信息

        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            table_name = self.get_table_name()
            sql = '''
            INSERT OR IGNORE INTO {} (usr_id, usr_name, usr_addr, url_icon) 
            VALUES (?,?,?,?)'''.format(table_name)
            for member in members:
                data = (
                    member.usr_id, 
                    member.usr_name, 
                    member.usr_addr, 
                    member.url_icon
                )
                self.get_cur().execute(sql, data)
        except Exception as e:
            raise Exception('insert_basic_infos: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def insert(self, members):
        """
        插入成员

        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            table_name = self.get_table_name()
            sql = 'INSERT OR IGNORE INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(table_name)
            for member in members:
                data = self.deconv_member(member)
                self.get_cur().execute(sql, data)
        except Exception as e:
            raise Exception('insert: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def delete(self, members):
        """
        按照usr_id删除成员

        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            # IMPROVE: 为什么没有办法直接excutemany??
            table_name = self.get_table_name()
            sql = 'DELETE FROM {} WHERE usr_id = ?'.format(table_name)
            for member in members:
                self.get_cur().execute(sql, [member.usr_id])
        except Exception as e:
            raise Exception('delete: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def update_infos(self, members):
        """
        按照id更新成员的其它信息

        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            table_name = self.get_table_name()
            sql = '''UPDATE {} SET 
            register_date = ?,com_likes = ?,group_num = ?,contacts_num = ?,rev_contacts_num= ?,
            stats_book_do = ?,stats_book_wish = ?,stats_book_collect = ?,
            stats_movie_do = ?,stats_movie_wish = ?,stats_movie_collect = ?,
            stats_music_do = ?,stats_music_wish = ?,stats_music_collect = ? WHERE usr_id = ?'''.format(table_name)
            for member in members:
                data = (
                    member.register_date,  #register_date
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
                    member.usr_id
                )
                self.get_cur().execute(sql, data)
        except Exception as e:
            raise Exception('update_infos: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def fetch_one_basic_infos(self):
        """
        获取表内一个数据的基本信息

        :return: 包含基本信息的GroupMember类实例
        :rtype: GroupMember
        """
        try:
            table_name = self.get_table_name()
            sql = 'SELECT usr_id, usr_name, usr_addr, url_icon FROM {} ORDER BY RANDOM() LIMIT 1'.format(table_name)
            member = self.get_cur().execute(sql).fetchone()
            return GroupMember(member[0], member[1], member[2], member[3])
        except Exception as e:
            raise Exception('fetch_one_basic_infos: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

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
            # IMPROVE: 更优雅的判断方式
            rowcount = len(self.get_cur().execute(sql,[usr_id]).fetchall())
            if rowcount >= 1:
                return True
            return False
        except Exception as e:
            raise Exception('is_existed_by_id: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def fetch_one_not_updated(self):
        """随机获取一个没有更新过首页信息的用户"""
        try:
            table_name = self.get_table_name()
            # FIXME: 因为用户来自小组，所以一定会有用户关注的小组数，后期应该添加一个属性来指示是否被更新过数据
            # 或者直接将更新后的数据插入到另一个表中，然后从当前表中删除...
            # TODO: 过滤用户？
            # 无头像：https://img1.doubanio.com/icon/user_normal.jpg
            # 无地址
            sql = 'SELECT usr_id, usr_name, usr_addr, url_icon FROM {} WHERE group_num = 0 ORDER BY RANDOM() LIMIT 1'.format(table_name)
            member = self.get_cur().execute(sql).fetchone()
            return GroupMember(member[0], member[1], member[2], member[3])
        except Exception as e:
            raise Exception('fetch_one_not_updated: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    def fecth_all_match_me(self):
        """
        过滤函数，找到匹配的用户
        """
        try:
            table_name = self.get_table_name()
            # TODO: 聚合分组操作
            sql = '''SELECT * FROM {}
            WHERE stats_book_collect >= 100
            '''.format(table_name)
            data = self.get_cur().execute(sql).fetchall()
            return data
        except Exception as e:
            raise Exception('fecth_match_me: {}'.format(e))
        finally:
            self.conn.commit()
            self.close_cur()

    @staticmethod
    def conv_member(data):
        """
        将查询到的数据恢复为GroupMember类的实例

        :param data: 从表中查询到的数据，元祖类型
        :type data: Tuple
        :return: 转换后的GroupMember类实例
        :rtype: GroupMember
        """
        member = GroupMember(data[0], data[1], data[2], data[3])
        member.update_infos(data[4:])
        return member

    @staticmethod
    def deconv_member(member):
        """
        将GroupMember类的实例转换为插入元祖

        :param member: GroupMember类实例
        :type member: GroupMember
        :return: 转换后的元祖类型，用于插入数据库中
        :rtype: Tuple
        """
        data = (
            member.usr_id,  #usr_id
            member.usr_name,  #usr_name
            member.usr_addr,  #usr_addr
            member.url_icon,  #url_icon
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
