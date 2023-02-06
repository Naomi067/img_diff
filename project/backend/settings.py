# -*- coding: utf-8 -*-

import os
from qaweb import config

# 本网站的根目录。一般就是project所在的目录。
# 如果当前是/srv/xxx/project/backend/目录的话，那就是/srv/xxx/
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CONFIG = {
    "BASE_PATH": BASE_PATH,
    "PROJECT_EN_NAME": "l32imagediff",
    "PROJECT_CH_NAME": "L32时装对比",
    "PRODUCT_IP": "10.240.120.97", ## todo 部署服务的ip，可以是str，list，set
    "HOST": "qa.leihuo.netease.com", ## todo 域名。如果没有，默认就是qa.leihuo.netease.com
    "PORT": 9979,
    "HTTPS": False,
    "SUPER_ADMINS": frozenset([ ## todo 超级管理员
        "wangxin7@corp.netease.com",
    ]),
    "DEVS": frozenset([ ## todo 开发人员，在非线上环境下，超级管理员名单会用此替换
        "wangxin7@corp.netease.com",
    ]),
    "ERROR_MSG_RECEIVER": frozenset([ ## todo 用来接收后端报错的人
        "wangxin7@corp.netease.com",
    ]),
    "RESOURCE_CONFIG_FILE": { ## todo 用于数据库账号密码、token等保密数据的存放，3个环境分开，这些文件不要提交svn
        config.ENV_DEV: "config_dev.json",
        config.ENV_TEST: "config_test.json",
        config.ENV_PRODUCTION: "config_production.json",
    },
    "LOGGERS": {
        # key是logger名称，定义后，后面可以根据logger.xxx.info() 这样的形式来调用
        # filename不需要写全路径，我都是往config.LOG_DIR 放的，也就是BASE_PATH/logs目录
        # 直接logger.info()，是打到default.log 中去的
        # 框架保留几个特殊名称（logger.RESERVED_LOGGERS），用于框架本身的log输出，如重名会报错
        "debug": {
            "level": "DEBUG",
            "filename": "debug.log",
            'backupCount': 1,
        },
    },
    "FEATURES": {
        "PROFILER": {  ## 打开qaweb_profiler功能
            "enable_env": [config.ENV_DEV, config.ENV_TEST],
            "username": "admin",
            "password": "123",
        },
        "APIDOC": {  ## 打开apidoc自动生成功能
            "enable_env": [config.ENV_DEV],
        },
        "COVERAGE": {  ## 打开覆盖率检查功能
            "enable": False,
            "auto_start": True,
            "auto_data": True, ## 重启时自动载入上一次覆盖率数据
        },
    },
    ## 以上是必填项目，以下是可选项
    "MAX_CONTENT_LENGTH": 10*1024*1024,  ## 默认使用qaweb.input_output.MAX_FILE_SIZE (20M)
}

## 初始化配置信息
config.Config(CONFIG)

## 以下是本网站自定义的一些常量配置
