# -*- coding: utf-8 -*-
import logging
from logging import handlers
from config import config


class Logger(object):
    """
    自定义封装logging模块
    """

    # 日志级别关系映射
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self, filename=config.get('logger', 'file_name'), level=config.get('logger', 'level')):
        # 默认设置
        fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        back_count = int(config.get('logger', 'backCount'))
        when = config.get('logger', 'when')
        self.logger = logging.getLogger(filename)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 往屏幕上输出
        sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        sh.setFormatter(format_str)
        # 往文件里写入，指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count, encoding='utf-8')
        # 设置文件里写入的格式
        th.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


log = Logger().logger


if __name__ == '__main__':
    pass
    # log = Logger().logger
    # log.error('error')
