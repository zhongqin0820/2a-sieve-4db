# 日期
文档创建：2019-08-29

`2a-sieve-4db`: **a**uto **a**miga **sieve** for [**d**ou**b**an](https://www.douban.com)

# 项目说明
爬虫练习，根据喜好，从豆瓣用户中过滤得到和自己具有一定匹配度的用户

# 目录说明
```
.
├── __init__.py
├── captcha.py                  #Deprecated：自动验证码识别
├── config.py                   #配置文件：与其相关的操作封装
├── config_example.ini          #配置文件：样例
├── crawler.py                  #爬虫：主逻辑
├── db.py                       #数据库：sqlite3数据库操作封装
├── group.py                    #爬虫：与小组成员页操作相关
├── img/                        #Deprecated：自动验证码识别的测试样例图片
├── logger.py                   #日志打印：与其相关的操作封装
├── table_members.py            #数据库：与小组成员表操作相关
└── user.py                     #相关类定义：豆瓣用户，书影音数据，小组成员类
```

# 使用说明
## 环境
- Python v3+
- `pip install -r requirement.txt`

## 修改配置文件
- 直接修改`config_example.ini`的文件名，或者`cp config_example.ini config.ini`新建一份
- 修改`config.ini`中对应的字段

## 运行
- `python crawler.py`
- 执行产生的文件：
    - `group.db`：对应的sqlite数据库文件
    - `default.log`：日志文件

# Changelog
- 2019-08-29: 创建文档并添加项目说明以及目录说明；添加使用说明
