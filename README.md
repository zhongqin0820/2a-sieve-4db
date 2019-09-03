# 日期
文档创建：2019-08-29

`2a-sieve-4db`: **a**uto **a**miga **sieve** for [**d**ou**b**an](https://www.douban.com)

# 项目说明
爬虫练习，出发点是：根据喜好，从豆瓣用户中过滤得到和自己具有一定匹配度的用户

这里的豆瓣用户可以是来自某个小组，某个（书影音）的主题下。也可以是自己的关注列表或被关注列表。

项目具有**较为完备的文档说明**：
```
docs/
├── CHANGELOG.md               #每个release版本的说明
├── GUIDE.md                   #项目所用的一些技术的学习路径以及参考资料说明
└── ROADMAP.md                 #项目规划说明
```

# 目录说明
```
.
├── Dockerfile                  #部署：Dockerfile
├── common/
│   ├── config.py               #配置文件：与其相关的操作封装，单例模式
│   ├── config_example.ini      #配置文件：样例
│   ├── db.py                   #数据库：sqlite3数据库操作封装
│   ├── logger.py               #日志打印：与其相关的操作封装，单例模式
│   └── user-agent.json         #配置文件：User-Agent池，用于生成随机User-Agent
├── engine/
│   └── crawler.py              #爬虫：主逻辑
├── model/
│   ├── common
│   │   └── user.py             #相关类定义：豆瓣用户，书影音数据，小组成员类，关注用户类
│   ├── contacts
│   │   ├── page.py             #网页解析：与关注列表页操作相关
│   │   └── table.py            #数据库：与关注列表页操作相关
│   ├── group
│   │   ├── page.py             #网页解析：与小组成员页操作相关
│   │   └── table.py            #数据库：与小组成员表操作相关
│   └── proxy
│       ├── page.py             #网页解析：与代理IP页相关
│       └── table.py            #数据库：与代理IP表相关
├── outputs/
│   ├── db/                     #程序输出：存放数据库文件
│   └── logs/                   #程序输出：存放日志文件
├── requirements.txt            #部署：通过pipreqs ./ --force覆盖生成的环境依赖文件
├── run.py                      #爬虫：执行入口文件
└── setup/
    ├── build.sh                #部署：根据Dockerfile构建镜像
    ├── pull.sh                 #部署：使用rsync将文件从远程同步到本地
    ├── push.sh                 #部署：用于将本地项目运行相关文件上传到远程服务器上
    ├── run.sh                  #部署：新建与run.py中相对应任务的容器
    └── setup.sh                #部署：在cent os的服务器上安装docker
```

# 使用说明
## 修改配置文件
- 直接修改`common/config_example.ini`的文件名为`common/config.ini`，或者`cp common/config_example.ini common/config.ini`新建一份
- 补充`config.ini`中对应的字段

## 环境
### 服务器
项目提供快速构建环境的一套脚本
- 本地执行：
    - `./setup/push.sh`：将项目相关执行文件上传到远程服务器
- 远程执行：
    - `sh ./setup/setup.sh`：安装docker环境并运行docker服务
    - `sh ./setup/build.sh`：根据Dockerfile构建镜像
    - `sh ./setup/run.sh`：根据`run.py`创建对应的容器并执行对应的内容

### 本地
- Python v3+
- `pip install -r requirement.txt`
- `python run.py <option>`：执行对应的可选项内容

## 执行产生的文件
可以使用`./setup/pull.sh`将运行结果和日志文件从远程同步到本地
```
outputs
├── db
│   ├── douban.db                 #对应的sqlite数据库文件
│   └── proxy.json                #爬到的代理IP数据，测试时产生的文件，可作单独使用
└── logs
    └── default.log               #日志输出文件
```

# Changelog
- 2019-08-29: 创建文档并添加项目说明以及目录说明；添加使用说明
- 2019-09-01: 添加项目文档说明，更新目录说明，更新使用说明
- 2019-09-02: 添加`pull.sh`的对应描述
- 2019-09-03: 补充对应结构化说明
