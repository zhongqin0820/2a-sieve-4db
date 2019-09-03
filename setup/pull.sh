#!/usr/bin/env bash
# 远程服务器
host="155.138.134.11"

# 要同步的文件，由于我们只需要同步db，因此只指定该文件
#file="outputs/db/douban.db"
#rsync -av -e ssh root@${host}:/workspace/${file} $(pwd)/${file}

# 同步所有远程的内容到本地，注意这里是一定会覆盖掉不一样的文件，所以本地做完修改的文件一定会被远程的文件覆盖
rsync -av -e ssh --exclude='__pycache__' \
root@${host}:/workspace/ $(pwd)/
