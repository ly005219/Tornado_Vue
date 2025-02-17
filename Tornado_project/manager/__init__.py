# 负责初始化项目

from tornado.web import Application

import peewee_async

from config import mysql, settings




## 配置数据库连接
db = peewee_async.PooledMySQLDatabase(**mysql)
# 创建异步数据库管理器
manager = peewee_async.Manager(db)
from router import handlers


def create_app():
    app = Application(handlers, **settings)
    app.listen(8000)
