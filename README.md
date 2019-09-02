# 日期
文档创建：2019-08-29

`2a-sieve-4db`: **a**uto **a**miga **sieve** for [**d**ou**b**an](https://www.douban.com)

# 项目说明
爬虫练习，出发点是：根据喜好，从豆瓣用户中过滤得到和自己具有一定匹配度的用户

这里的豆瓣用户可以是来自某个小组，某个（书影音）的主题下。也可以是自己的关注列表或被关注列表。

项目具有**较为完备的文档说明**，如：
```
.
├── CHANGELOG.md               #每个release版本的说明
├── GUIDE.md                   #项目所用的一些技术的学习路径以及参考资料说明
├── README.md
└── ROADMAP.md                 #项目规划说明
```

# 目录说明
```
.
├── Dockerfile                  #部署：Dockerfile
├── build.sh                    #部署：在cent os的服务器上安装docker，并根据Dockerfile构建镜像
├── __init__.py
├── config.py                   #配置文件：与其相关的操作封装，单例模式
├── config_example.ini          #配置文件：样例
├── crawler.py                  #爬虫：主逻辑
├── deploy.sh                   #部署：用于将本地项目运行相关文件上传到远程服务器上
├── db.py                       #数据库：sqlite3数据库操作封装
├── logger.py                   #日志打印：与其相关的操作封装，单例模式
├── page_contacts.py            #爬虫：与关注列表页操作相关
├── page_group.py               #爬虫：与小组成员页操作相关
├── page_proxy.py               #爬虫：与代理IP爬取相关
├── pull.sh                     #部署：使用rsync将文件从远程同步到本地
├── requirements.txt            #部署：通过pipreqs ./ --force覆盖生成的环境依赖文件
├── run.py                      #爬虫：入口文件
├── run.sh                      #部署：新建与run.py中相对应任务的容器
├── table_contacts.py           #数据库：与关注列表页操作相关
├── table_members.py            #数据库：与小组成员表操作相关
├── table_proxy.py              #数据库：与代理IP爬取相关
├── user-agent.json             #配置文件：User-Agent池，用于生成随机User-Agent
└── user.py                     #相关类定义：豆瓣用户，书影音数据，小组成员类，关注用户类
```

# 使用说明
## 修改配置文件
- 直接修改`config_example.ini`的文件名，或者`cp config_example.ini config.ini`新建一份
- 修改`config.ini`中对应的字段

## 环境
### 服务器
项目提供快速构建环境的一套脚本
- 本地执行：`./deploy.sh`将项目相关执行文件上传到远程服务器
- 远程执行：
    - `./build.sh`：安装docker, 根据Dockerfile构建镜像
    - `./run.sh`：根据run.py创建对应的容器并执行对应的内容

### 本地
- Python v3+
- `pip install -r requirement.txt`
- `python run.py`：执行

## 执行产生的文件
可以使用`pull.sh`将运行结果和日志文件从远程同步到本地
- `douban.db`：对应的sqlite数据库文件
- `default.log`：对应的日志文件

# Changelog
- 2019-08-29: 创建文档并添加项目说明以及目录说明；添加使用说明
- 2019-09-01: 添加项目文档说明，更新目录说明，更新使用说明
- 2019-09-02: 添加`pull.sh`的对应描述
