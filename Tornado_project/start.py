#负责启动项目
from tornado.ioloop import IOLoop
from manager import create_app,manager
from manager.models import *
from uuid import uuid4

def start():
    create_app()
    IOLoop.current().start()

def create_table():
    FollowModel.create_table(True)

async def add_user():
    await manager.create(User,
        id=uuid4(),
        email='123@qq.com',
        password='123456',

    )



if __name__ == '__main__':
    start()
    #create_table()
    #IOLoop.current().run_sync(add_user)