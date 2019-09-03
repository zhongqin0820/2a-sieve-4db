# Changelog
## [Unreleased] - 2019-09-03
### 添加
- 项目部署
    - pull.sh：使用rsync将文件从远程同步到本地

### 更换
- 结构化项目文件，使项目结构更清晰
- 部署时，将环境搭建与镜像构建分开

### FIXED
- 运行容器时根据不同的option指定不同的运行内容

## [0.0.2] - 2019-09-01
### 添加
- 项目雏形
    - 符合基本需求，可以work的代码
    - 代码分格：.editorconfig
- 文档
    - README.md
    - 版本说明: CHANGELOG.md
    - 项目指导：GUIDE.md
- 功能
    - 与小组成员页相关内容的爬取
    - 与关注列表页相关内容的爬取
    - 与用户公开主页相关内容的爬取
    - user-agent与代理IP相关
- 项目部署
    - deploy.sh：将文件同步到服务器
    - build.sh：安装docker，同时构建镜像
    - run.sh：启动对应的容器
    - run.py：执行入口
    - Dockerfile：主要的逻辑位于run.py
    - requirements.txt：必要的环境
    - config.ini：配置文件

### 更换
- Logger：使用logging模块的自定义封装代替之前的缓冲区Logger，并使用单例模式
- 结构化文件名，使项目文档更清晰

### FIXED
- 拼写错误
- members表的Update操作
- Config：替换为单例模式

### 弃用
- 伪需求：自动二维码识别，目前的准确度太低

## [0.0.1] - 2019-08-29
### 添加
- 必要的项目基本文档
    - README.md
    - ROADMAP.md
    - LICENSE
    - .editorconfig

[Unreleased]: https://github.com/zhongqin0820/2a-sieve-4db
[0.0.2]: https://github.com/zhongqin0820/2a-sieve-4db/releases/tag/v0.0.2
[0.0.1]: https://github.com/zhongqin0820/2a-sieve-4db/releases/tag/v0.0.1
