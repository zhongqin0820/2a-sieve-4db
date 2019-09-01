# 说明
记录项目的一些参考文档以及对应的功能点都是怎么做出来的

# 项目规范
- [Python项目自动生成requirements.txt](https://blog.csdn.net/bailixuance/article/details/84436460)
- [Git代码行数统计命令](https://www.cnblogs.com/supiaopiao/p/10943882.html)
- [如何把微信二维码藏进命令行里](https://blog.wolfogre.com/posts/qrcode-in-shell/)
- [Python Docstring 风格和写法学习](https://www.cnblogs.com/ryuasuka/p/11085387.html)：项目使用reST风格
- [python导入自定义模块和包](https://www.cnblogs.com/telazy/p/8967515.html)

## 关于错误处理
- 一个原则就是谁调用，谁处理错误
- log模块的信息只能利用`.format`输出字符串

# 项目参考
除了本身之前做的lezen1需要有这种功能之外，在搜索准备过程中，还参考了如下的一些内容：

## 侃大山讨论
- [豆瓣上的人和你有多少共同爱好呢？](https://www.douban.com/group/topic/22024189/)
- [关于豆瓣共同喜好的一点小感悟](https://www.douban.com/note/259736940/?type=like)
- [怎么在豆瓣上，和自己共同爱好最多的人？](https://www.douban.com/group/topic/10844186/)

## 实践讨论
- [写了个程序来抓取共同喜好，有小伙伴一起来完善吗](https://www.douban.com/group/topic/65642322/)
- [豆瓣上谁和你共同喜好最多？](https://www.douban.com/note/380153149/)

### 强相关讨论+Repo
- [Sky组非官方用户行为分析](https://www.douban.com/group/topic/86190345/)
- [fionanotblack/douban_group_crawler](https://github.com/fionanotblack/douban_group_crawler)：给大佬递茶

### Github相关repo
- [xiazcx/douban_seek](https://github.com/xiazcx/douban_seek)：非常朴素，并且已经无法work了
- [haithink/doubanSpyder](https://github.com/haithink/doubanSpyder)：非常朴素，可以简单work

# 项目特性
## 自动验证码
**实践后发现正确率太低，同时发现属于伪需求，因此弃用**，不过挺有趣的，可以等以后再优化
- [豆瓣网登录之验证码识别](https://www.deeplearn.me/808.html)
- [Python 豆瓣网的全自动登录（豆瓣验证码自动识别）](https://blog.csdn.net/az9996/article/details/86064122)

### 扩展自动验证码
- [Python+Selenium+PIL+Tesseract真正自动识别验证码进行一键登录](https://blog.csdn.net/mrlevo520/article/details/51901579)

### pytesseract相关
- [mac python 配置pytesseract](https://blog.csdn.net/jianglianye21/article/details/78280643)
- [python pytesseract psm 选项参数](https://blog.csdn.net/huitailangyz/article/details/80390090)
- [tesseract-ocr怎么设置只匹配数字+大写字母](https://zhidao.baidu.com/question/264485819614542605.html)
- [Mac安装brew并更改源](https://www.jianshu.com/p/22820319f71b)

## 提取页面内容
### BeautifulSoup
- [python bs4解析网页时 bs4.FeatureNotFound](https://blog.csdn.net/qq_34215281/article/details/77714584)
- [股票数据定向爬虫时出现 AttributeError: 'NoneType'](https://blog.csdn.net/qq_36525166/article/details/81258168)
- [bs4 里提取a标签里的坑啊](https://blog.csdn.net/zqinstarking/article/details/79941606)

### 正则表达式
- [Python正则表达式匹配日期与时间](https://www.cnblogs.com/OnlyDreams/p/7845527.html)

## SQLite
根据数据结构，掌握如何正确定义表结构；针对表的操作掌握对应CRUD的方法，做到心有CRUD，自然就能够写出CRUD。
- [sqlite 的数据类型 与 python 的数据类型](https://blog.csdn.net/lengyff/article/details/45076903)
- [SQlite3插入(insert into)多个变量](https://blog.csdn.net/qq_35531549/article/details/88209267)
- [SQLite Update 语句](https://www.runoob.com/sqlite/sqlite-update.html)
- [让 Python 更加充分的使用 Sqlite3](https://www.cnblogs.com/xyou/p/8294982.html)：掌握sqlite3的API中的基本概念
- [smileboywtu/SQLite3: Learn SQLite3 in Python3](https://github.com/smileboywtu/SQLite3)

## 配置文件
- [python读取配置文件&&简单封装](https://www.cnblogs.com/hanmk/p/9843136.html)
- [Python项目读取配置的几种方式](https://www.cnblogs.com/zhangyafei/p/10265072.html)
- [python配置文件读取](https://www.cnblogs.com/ianduin/p/8510353.html)

# 扩展参考
## 使用代理IP
- [https://proxy.coderbusy.com/](https://proxy.coderbusy.com/)：提供代理IP
- [python豆瓣多线程爬虫加IP代理（免费的一般是不稳定）](https://juejin.im/post/5bcecd2a6fb9a05d212ed64a)：很好的教程帖
- [如何突破豆瓣爬虫限制频率？](https://www.v2ex.com/t/260777)：侃大山讨论
- [ip被豆瓣封禁了怎么办](https://www.douban.com/group/topic/4742710/)：水帖

## 并发编程
- [python异步编程之asyncio（百万并发）](https://www.cnblogs.com/shenh/p/9090586.html)

## 数据分析
- [Python地理位置信息库geopy的使用（一）：基本使用](https://blog.csdn.net/SanCava/article/details/82757761)：用于从地址获取经纬度信息等
- [DQinYuan/chinese_province_city_area_mapper](https://github.com/DQinYuan/chinese_province_city_area_mapper)：一个用于提取简体中文字符串中省，市和区并能够进行映射，检验和简单绘图的python模块

## 自动化测试
- [(3) 【自动化测试】Python - unittest单元测试框架 - python学习+自动化测试实践](https://segmentfault.com/a/1190000016315201)

## Scrapy框架
- [Python->用Scrapy爬取豆瓣电影](https://my.oschina.net/tedzheng/blog/800833)
- [Scrapy 爬虫实例 抓取豆瓣小组信息并保存到mongodb中](https://blog.51cto.com/1992mrwang/1583539)
- [【爬虫实践】爬虫获取豆瓣用户粉丝信息](https://blog.csdn.net/qq_36803928/article/details/84001202)

# 其它项目无关的扩展
## 自动豆邮
## 自动回帖/顶帖

# Changelog
- 2019-08-30：创建文档，第一版内容
- 2019-08-31：添加[强相关讨论+Repo](#强相关讨论+Repo)
