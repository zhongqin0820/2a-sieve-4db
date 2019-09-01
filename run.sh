#!/usr/bin/env bash
# 执行爬虫
# -d后台运行爬虫容器，注意此处挂载的容器卷内容
#docker run -d -v "$PWD":/usr/src/app -it --name crawl douban
# --rm 执行后删除容器
docker run -d -v "$PWD":/usr/src/app -it --rm --name crawl douban
# 查看容器的控制台log
#docker logs crawl | tail
# 暂停容器
#docker stop crawl
# 启动暂停的容器
#docker start crawl
# 进入容器
#docker attach crawl

# 查看数据库内容
# 需要在run.py中修改对应逻辑，新建容器即可
#docker run -v "$PWD":/usr/src/app -it --rm --name table douban

# proxy
#docker run -v "$PWD":/usr/src/app -it --rm --name proxy douban

# single script
#docker run -it --name crawl -v "$PWD":/usr/src/app -w /usr/src/app python:3 python table_members.py
