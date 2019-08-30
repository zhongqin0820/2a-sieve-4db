# -*- coding: utf-8 -*-
import time
from db import DBHandler
from user import GroupMember


class MembersTable(DBHandler):
    """
    与小组成员表相关的CRUD操作
    """
    def __init__(self, db_addr='', table_name=''):
        super(MembersTable, self).__init__(db_addr, table_name)

    def create(self):
        """
        创建小组成员表
        """
        try:
            sql = '''
            CREATE TABLE `members` (
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
            )'''
            self.get_cur().execute(sql)
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            print(e)

    def insert_basic_infos(self, members):
        """
        插入成员的基本信息
        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            table_name = 'members'
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
                self.conn.commit()
            self.close_cur()
        except Exception as e:
            print(e)

    def insert(self, members):
        """
        插入成员
        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            table_name = 'members'
            sql = 'INSERT OR IGNORE INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(table_name)
            for member in members:
                data = self.deconv_member(member)
                self.get_cur().execute(sql, data)
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            print(e)

    def delete(self, members):
        """
        按照usr_id删除成员
        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            # IMPROVE: 为什么没有办法直接excutemany??
            table_name = 'members'
            sql = 'DELETE FROM {} WHERE usr_id = ?'.format(table_name)
            for member in members:
                self.get_cur().execute(sql, [member.usr_id])
                self.conn.commit()
            self.close_cur()
        except Exception as e:
            print(e)

    def update_infos(self, members):
        """
        按照id更新成员的其它信息
        :param members: GroupMember类型的实例列表
        :type members: List[GroupMember]
        """
        try:
            table_name = 'members'
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
                )
                self.get_cur().execute(sql, data)
            self.conn.commit()
            self.close_cur()
        except Exception as e:
            print(e)

    def fetch_one_basic_infos(self):
        """
        获取表内一个数据的基本信息
        :return: 包含基本信息的GroupMember类实例
        :rtype: GroupMember
        """
        try:
            table_name = self.table_name
            sql = 'SELECT usr_id, usr_name, usr_addr, url_icon FROM {}'.format(table_name)
            member = self.get_cur().execute(sql).fetchone()
            self.conn.commit()
            self.close_cur()
            return GroupMember(member[0],member[1],member[2],member[3])
        except Exception as e:
            print(e)
            return None

    def is_existed_by_id(self, usr_id):
        """
        根据ID判断是否在表内

        :param usr_id: 用户ID
        :type usr_id: str
        :return: True表示存在，反之不存在
        :rtype: bool
        """
        try:
            table_name = self.table_name
            sql = 'SELECT usr_id FROM {} WHERE usr_id = ?'.format(table_name)
            # IMPROVE: 更优雅的判断方式
            rowcount = len(self.get_cur().execute(sql,[usr_id]).fetchall())
            if rowcount >= 1:
                return True
            self.conn.commit()
            self.close_cur()
            return False
        except Exception as e:
            print(e)
            return False

    def fecth_match_me(self):
        """
        过滤函数，找到匹配的用户
        """
        try:
            table_name = self.table_name
            # 聚合分组操作
            sql = '''SELECT * FROM {}
            WHERE stats_book_collect >= 100
            '''.format(table_name)
            data = self.get_cur().execute(sql).fetchall()
            self.conn.commit()
            self.close_cur()
            return data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def conv_member(data):
        """
        将查询到的数据恢复为GroupMember类的实例

        :param data: 从表中查询到的数据，元祖类型
        :type data: Tuple
        :return: 转换后的GroupMember类实例
        :rtype: GroupMember
        """
        member = GroupMember(data[0],data[1],data[2],data[3])
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


if __name__ == '__main__':
    members = MembersTable()
    # 测试当前条目数
    items = members.fetch_all()
    num_before_insert = len(items)
    print('当前共有: ', num_before_insert)
    # 打印条目
    for item in items[:3]:
        member = members.conv_member(item)
        member.print_infos()
        # member.print_basic_infos()
        print()

    # 测试将元祖数据转换为GroupMember实例后，插入数据的功能
    items = [
    ('usr_id_existed_1', 'usr_id_existed_1', '北京', 'https://img3.doubanio.com/icon/usr_id_existed_1.jpg',
    '2006-05-05', 36, 136, 247, 251, 2, 14, 50, 4, 82, 582, 0, 2, 96),
    ('usr_id_existed_2', 'usr_id_existed_2', '北京', 'https://img3.doubanio.com/icon/usr_id_existed_2.jpg',
    '2006-05-12', 33, 15, 84, 292, 7, 216, 150, 5, 225, 831, 0, 0, 108),
    ('usr_id_existed_3', 'usr_id_existed_3', '昆明', 'https://img1.doubanio.com/icon/usr_id_existed_3.jpg',
    '2005-12-03', 36, 243, 395, 144, 16, 124, 127, 6, 501, 1118, 16, 19, 14)
    ]
    for item in items:
        members.insert([members.conv_member(item)])

    # 测试判断ID是否存在
    tests = [("usr_id_not_existed", False), ("usr_id_existed_1", True)]
    try:
        for test in tests:
            if members.is_existed_by_id(test[0]) is not test[1]:
                raise('expected {}, got {}'.format(test[1], not test[1]))
    except Exception as e:
        print(e)
        print('测试失败：判断用户是否存在')
    print('测试通过：判断用户是否存在')

    # 测试删除用户: usr_id_existed_1
    members.delete([members.conv_member(items[0])])
    # 测试判断删除的用户ID是否存在
    test = ("usr_id_existed_1", False)
    if members.is_existed_by_id(test[0]) is not test[1]:
        print('expected {}, got {}'.format(test[1], not test[1]))
        print('测试失败：删除用户usr_id_existed_1')
    else:
        print('测试通过：删除用户usr_id_existed_1')

    # 测试删除剩余mock数据
    for item in items:
        members.delete([members.conv_member(item)])
    items = members.fetch_all()
    num_after_delete = len(items)
    if num_after_delete != num_before_insert:
        print('expected {}, got {}'.format(num_before_insert, num_after_delete))
        print('测试失败：删除剩余用户')
    else:
        print('测试通过：删除剩余用户')

    # 查询过滤后的用户
    items = members.fecth_match_me()
    print()
    print('----------------------------------------------------------------------------------')
    print('过滤得到的用户数: ', len(items))
    for item in items:
        member = members.conv_member(item)
        member.print_infos()
        # member.print_basic_infos()
        print()

    # 删除表，新建表
    # members.dropTable()
    # members.create()
