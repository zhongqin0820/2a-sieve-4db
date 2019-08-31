import requests
from time import sleep
from lxml import etree
import json
import os
import time
from config import Config
from logger import Logger
log = Logger().logger


class ProxyItem(object):
    def __init__(self, ip_port, create_date=time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d"), is_valid=True):
        super(ProxyItem, self).__init__()
        self.ip_port = ip_port
        self.create_date = create_date
        self.is_valid = is_valid

    def valid_proxy(self, headers=''):
        """
        验证代理IP是否有效

        :param headers: 请求头
        :type headers: dict
        :return: 是否有效
        :rtype: bool
        """
        url = Config().get('proxy', 'test_url')
        proxies = {
            'http': 'http://' + self.ip_port
        }
        if headers is '':
            headers = {
                Config().get('headers', 'user_agent_info'): Config().get_ua()
            }
        try:
            r = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies, timeout=20)
            if r.status_code == 200:
                self.is_valid = True
            else:
                self.is_valid = False
                log.info(r.text)
        except Exception as e:
            log.error('{} failed: {}'.format(self.ip_port, e))
        return self.is_valid

    def print_infos(self):
        """打印条目信息"""
        print('IP: {}\t 创建于: {}\t 有效性: {}'.format(self.ip_port, time.strftime("%Y-%m-%d", self.create_date), self.is_valid))

    def serialize(self):
        """
        序列化方便json.dump

        :return: 序列化后的条目
        :rtype: dict
        """
        return {
            "ip_port": self.ip_port, 
            "create_date": time.strftime("%Y-%m-%d", self.create_date), 
            "is_valid": self.is_valid
        }


class ProxyList(object):
    def __init__(self):
        self.url = Config().get('proxy', 'page_url') + '/{0}'
        self.headers = {
            Config().get('headers', 'user_agent_info'): Config().get_ua()
        }
        self.json_file = Config().get('proxy', 'file_name')

    def get_page_url(self, page_num):
        """拼接得到代理IP页"""
        return self.url.format(page_num)

    def get_page_selector(self, page_num):
        """获取对应代理IP页的内容"""
        url = self.get_page_url(page_num)
        try:
            r = requests.get(url, headers=self.headers).text
            selector = etree.HTML(r)
            sleep(2)
        except Exception as e:
            log.error('get xicidaili page faild....', e)
        return selector

    def get_proxies_from_page(self, page_num):
        """获取代理IP"""
        try:
            proxies=[]
            selector = self.get_page_selector(page_num)
            ip_list = selector.xpath('//table[@id="ip_list"]')[0]
            for each in ip_list[1:]:
                ip =  each.xpath('td[2]/text()')[0]
                port = each.xpath('td[3]/text()')[0]
                ip_port = ip+':'+port
                proxy = ProxyItem(ip_port)
                if proxy.valid_proxy(self.headers):
                    proxies.append(proxy)
        except Exception as e:
            log.error('analysis xicidaili faild...',e)
        return proxies

    def crawl(self):
        return self.get_proxies_from_page(1)

    def save(self, page_nums):
        for page_num in range(1, page_nums+1):
            proxies = self.get_proxies_from_page(page_num)
            print('有效IP数目', len(proxies))
            proxies = [proxy.serialize() for proxy in proxies]
            with open(self.json_file, 'a') as f:
                json.dump(proxies, f, sort_keys=True, indent =4, separators=(',', ': '),ensure_ascii=True)

    def test(self):
        if os.path.isfile(self.json_file):
            os.remove(self.json_file)
            self.save(1)
        else:
            self.save(1)


if __name__=='__main__':
    p = ProxyList()
    p.test()
