from re import T
from manager.handler.BaseHandler import BaseHandler
from manager import manager
from manager.models import TopicModel,User,CollectionModel
from manager.decorators import login_required_async

class AddCollectionHandler(BaseHandler):
    @login_required_async
    async def post(self):
        topic_id = self.get_body_argument('id')
        # 获取帖子信息
        topic = await manager.get(TopicModel,id = topic_id)
        # 获取用户信息
        user = await manager.get(User,id = self._user_id)
        # 创建对象并保存
        await manager.create(CollectionModel,topic = topic,user= user)
        self.finish({'code':200,'msg':'收藏成功!'})


class GetMyCollectionHandler(BaseHandler):
    @login_required_async
    async def post(self):
        # 通过userId获取收藏的信息
        collection = await manager.execute(CollectionModel.select().join(User).where(User.id == self._user_id))
        data = []
        for c in collection:
            tc = c.to_json()
            tc['user'] = c.user.to_json()
            tc['topic'] = c.topic.to_json()
            del tc['topic']['user']
            del tc['topic']['imgs']
            del tc['topic']['content']
            data.append(tc)
        self.finish({'code':200,'msg':'获取个人收藏成功!','collection':data})

class DeleteMyCollectionHandler(BaseHandler):
    @login_required_async
    async def post(self):
        topic_id = self.get_body_argument('id')
        # 通过userid获取用户
        user = await manager.get(User,id =self._user_id)
        # 通过topic获取帖子
        topic = await manager.get(TopicModel,id = topic_id)
        # 通过userid进行删除数据
        rs = await manager.execute(CollectionModel.delete().where(CollectionModel.user == user,CollectionModel.topic == topic))
        if rs>0:
            self.finish({'code':200,'msg':'删除收藏成功'})
        else:
            self.finish({'code':500,'msg':'删除收藏失败'})
