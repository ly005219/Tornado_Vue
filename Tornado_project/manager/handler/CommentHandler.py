from uuid import uuid4

from manager.handler.BaseHandler import BaseHandler
from manager import manager
from manager.models import TopicModel,CommentModel, User
from manager.decorators import login_required_async

class GetCommentHandler(BaseHandler):
    async def post (self):
        rs_data = {}
        id = self.get_body_argument('id')
        # 根据帖子ID获取所有的评论
        comments = await manager.execute(CommentModel.select().join(TopicModel).where(TopicModel.id == id))

        data = []
        # 遍历评论，转换成JSON
        for c in comments:
            tc = c.to_json()  # 把评论转成json
            tc['user'] = c.user.to_json() # 往转换成的json对象中增加user属性
            del tc['topic']
            data.append(tc)
        rs_data['code'] = 200
        rs_data['msg'] = '获取评论成功'
        rs_data['comments'] = data
        self.finish(rs_data)


class AddCommentHandler(BaseHandler):
    @login_required_async
    async def post(self):
        content = self.get_body_argument('content')
        topic_id = self.get_body_argument('topic_id')
        # 获取帖子对象信息
        topic = await manager.get(TopicModel,id = topic_id)
        # 获取用户对象信息
        user = await manager.get(User,id = self._user_id)
        # 创建一个Comment对象
        await manager.create(CommentModel,id = uuid4(),content = content,topic = topic, user = user)
        self.finish({'code':200,'msg':'评论成功！'})

class GetMyCommentHandler(BaseHandler):
    @login_required_async
    async def post(self):
        # 获取评论
        comments = await manager.execute(CommentModel.select().join(User).where(User.id == self._user_id))
        # 建立一个列表，来存储所有的评论数据<json类型>
        data = []
        # 遍历数据，将数据转成json类型
        for c in comments:
            tc = c.to_json()
            tc['user'] = c.user.to_json()
            del tc['topic']
            data.append(tc)
        self.finish({'code':200,'msg':'获取个人评论成功！','comments':data})
