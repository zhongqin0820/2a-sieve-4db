#!/usr/bin/env bash
# 配置运行环境
# 安装docker
yum install docker -y

# 启动docker
systemctl start docker

# 构建镜像，当需要执行不同逻辑时，只需要修改run.py中的执行内容后新建不同的容器即可
docker build -t douban .
