#!/usr/bin/env bash
# Step 1: 上传本地文件到远程
# 服务器IP
host="144.202.111.223"
# 同步上传文件
rsync -av -e ssh --exclude='docs/' \
--exclude='stash/' --exclude='__pycache__/' \
--exclude='.idea/' --exclude='.git/' \
--exclude='.DS_Store' --exclude='*.md' \
$(pwd)/ root@${host}:/workspace --delete

# Step 2: 在远程服务器依次执行
# ./build.sh # 安装docker, 构建镜像
# sh run.sh # 根据run.py创建对应的容器
