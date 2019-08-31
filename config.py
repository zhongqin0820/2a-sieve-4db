# -*- coding: utf-8 -*-
import configparser
import json
import random


class Config(object):
    """
    从ini文件中读取配置信息
    """
    def __init__(self, file_name='config.ini'):
        """
        :param file_name: ini配置文件所在路径: /path/to/config.ini
        :type file_name: str
        :raise: IndexError
        """
        super(Config, self).__init__()
        self.file_name = file_name
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.file_name)
            self.section = self.config.sections()[0]
        except Exception as e:
            raise e

    def use_section(self, section=''):
        """
        切换section

        :param section: ini配置文件中用[]标识的内容
        :type section: str
        """
        if section is not '':
            self.section = section

    def get(self, section='', option=''):
        """
        根据传入的section获取对应的option的value

        :param section: ini配置文件中用[]标识的内容
        :param option: 对应[section]下的option
        :type section: str
        :type option: str
        :return: 对应option的值
        :rtype: str
        :raise: configparser.NoSectionError, AttributeError
        """
        try:
            if section is '':
                section =  self.section
            return self.config.get(section=section, option=option)
        except Exception as e:
            raise e

    def sections(self):
        """
        获得配置文件中的所有支持的section

        """
        return self.config.sections()

    def options(self, section=''):
        """
        获得对应section的所有option

        :param section: ini配置文件中用[]标识的内容
        :type section: str
        :raise: configparser.NoSectionError, AttributeError
        """
        try:
            if section is '':
                section = self.section
            return self.config.options(section)
        except Exception as e:
            raise e

    def items(self, section=''):
        """
        获得对应section的所有<option,value>对

        :param section: ini配置文件中用[]标识的内容
        :type section: str
        :return: 对应section的所有<option,value>对
        :rtype: List[(str,str)]
        :raise: configparser.NoSectionError, AttributeError
        """
        try:
            if section is '':
                section = self.section
            return self.config.items(section)
        except Exception as e:
            raise e

    def get_ua(self):
        """
        返回一个随机的User-Agent

        :return: 一个User-Agent
        :rtype: str
        :raise: AttributeError
        """
        file_name = self.config.get('headers', 'user_agent_file')
        try:
            with open(file_name, 'r') as f:
                user_agent = json.load(f)
        except Exception as e:
            raise e
        else:
            key = random.choice(list(user_agent.keys()))
            ua = random.choice(user_agent[key])
            return ua


if __name__ == '__main__':
    """
    测试config的配置，config.ini下的内容应为
    [mysql]
    host = 127.0.0.1
    port = 3306
    user = root
    password = root
    database = test
    """
    # 测试随机读取ua
    c = Config()
    print(c.get_ua())
    # # 测试其它操作
    # s = c.get(section="mysql", option="host")
    # print(s)
    # s = c.get(section="mysql", option="port")
    # print(s)
    # # 设置section
    # c.use_section("mysql")
    # s = c.get(option="user")
    # print(s)
    # s = c.get(option="password")
    # print(s)
    # s = c.get(option="database")
    # print(s)
