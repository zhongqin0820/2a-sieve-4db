#!/usr/bin/env bash
# 根据Dockerfile构建镜像，镜像名为douban
# 当需要执行不同逻辑时，只需要运行不同的容器时指定对应可选项的值
docker build -t douban .
