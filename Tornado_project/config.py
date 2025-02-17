import os

base_path = os.path.abspath(os.path.dirname(__file__))
# 配置一下settings
settings = {
    "static_path": os.path.join(base_path, "manager/static"),
    "static_url_prefix": "/static/",
    "debug": True,
}

mysql = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "tornado_project",
}

email={
    'host':'2577265832@qq.com',
    'pwd':'oezalutdpbpjebec'

}

secret='qwetyuio'

jwt_exp=3600#token过期时间,单位秒