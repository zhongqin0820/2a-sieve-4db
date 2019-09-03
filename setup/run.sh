#!/usr/bin/env bash
# run.py 中定义的可选项
# Usage:
#     python run.py <option>
# Options:
#     1 - 测试config
#     2 - 测试logger
#     3~4 - 与代理IP相关
#         3 - 测试代理IP拉取
#         4 - 随机打印一个代理IP的信息
#     5~8 - Engine相关操作
#         5 - 测试登录操作
#         6 - 拉取关注列表页数据
#         7 - 拉取小组成员页数据
#         8 - 从小组成员表中更新数据到用户表中
#     9~12 - 数据库查询相关操作
#         9 - 测试数据库连接
#         10 - 打印拉取到的小组成员页数据
#         11 - 打印拉取到的关注列表页数据
#         12 - 随机打印一个打印从成员表中过滤得到的用户

# 通过对应的可选项构建不同的容器执行，这里的douban是镜像名
# docker run -v "$PWD":/usr/src/app -it --rm --name <container_name> douban <option>
# 常见容器可选项说明
# -d后台运行容器，注意此处-v挂载的容器卷内容；
# -it表示交互式执行，--name指定容器名为：<container_name>
# --rm 执行后删除容器
#docker run -d -v "$PWD":/usr/src/app -it --rm --name <container_name> douban
# 查看-d后台运行容器的控制台log
#docker logs <container_name> | tail -15
# 暂停容器
#docker stop <container_name>
# 启动暂停的容器
#docker start <container_name>
# 进入容器
#docker attach <container_name>

# 单个脚本，不构建镜像
#docker run -it --name single -v "$PWD":/usr/src/app -w /usr/src/app python:3 python

# 执行爬虫
# docker run -d -v "$PWD":/usr/src/app -it --name crawl douban 7
# 查看所爬小组成员表内容
#docker run -v "$PWD":/usr/src/app -it --rm --name table douban 10
# 查看代理相关内容
#docker run -v "$PWD":/usr/src/app -it --rm --name proxy douban 4

