#!/usr/bin/env bash
# Step 1: 上传本地文件到远程
# 服务器IP
host="136.244.85.192"
# 同步上传文件
rsync -av -e ssh --exclude='__docs/' --exclude='docs/' \
--exclude='__stash/' --exclude='__pycache__/' \
--exclude='.idea/' --exclude='.git/' \
--exclude='.DS_Store' --exclude='*.md' \
--exclude='.editorconfig' --exclude='.gitignore' \
--exclude='LICENSE' \
$(pwd)/ root@${host}:/workspace --delete

# Step 2: 在远程服务器依次执行
# sh setup/build.sh # 安装docker, 构建镜像
# sh setup/run.sh # 根据run.py创建对应的容器
