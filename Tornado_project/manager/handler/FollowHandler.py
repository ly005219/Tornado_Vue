from json import loads

from manager.handler.BaseHandler import BaseHandler
from manager import manager
from manager.models import User, FollowModel
from manager.decorators import login_required_async


class AddFollowHandler(BaseHandler):
    @login_required_async
    async def post(self):
        try:
            # 获取关注的用户ID
            uid = self.get_body_argument("id")
            to_user = await manager.get(User, id=uid)
            # 获取自己的ID
            from_user = await manager.get(User, id=self._user_id)
            # 增加关注关系
            await manager.create(FollowModel, to_user=to_user, from_user=from_user)
            self.finish({"code": 200, "msg": "关注成功！"})
        except Exception as e:
            self.finish({"code": 500, "msg": "关注失败！"})


class GetFollowHandler(BaseHandler):
    @login_required_async
    async def post(self):
        try:
            # 获取关注的用户ID
            uid = self.get_body_argument('id')
            fid = self._user_id

            # 在数据库查询是否已关注
            follow  = await manager.execute(FollowModel.select().where(FollowModel.to_user == uid,FollowModel.from_user == fid))
            if follow:
                self.finish({'code':200,'msg':'已关注','flag':True})
            else:
                self.finish({'code':200,'msg':'未关注','flag':False})
        except Exception as e:
            print(e)
            self.finish({'code':200,'msg':'未关注','flag':False})
    @login_required_async
    async def get(self):
        # user.id pic nick_name create_time
        follows = await manager.execute(FollowModel.select(FollowModel.create_time,User.id,User.pic,User.nick_name).join(User,on=FollowModel.to_user).where(FollowModel.from_user == self._user_id))
        # data = []
        # for f in follows._rows:
        #     tf={'create_time':str(f[0]),'id':f[1],'pic':f[2],'nick_name':f[3]}
        #     data.append(tf)

        data = [{'create_time':str(f[0]),'id':f[1],'pic':f[2],'nick_name':f[3]} for f in follows._rows ]
        
        self.finish({'code':200,'msg':'获取关注成功！','friends':data})


class DeleteFollowHandler(BaseHandler):
    @login_required_async
    async def delete(self):
        try:
            data = loads(self.request.body)
            uid = data.get('id')
            to_user = await manager.get(User,id = uid)
            from_user = await manager.get(User,id = self._user_id)
            # rs = await manager.execute(FollowModel.delete().where(FollowModel.to_user == to_user,FollowModel.from_user == from_user))
            rs = await manager.execute(FollowModel.delete().where(FollowModel.to_user == uid,FollowModel.from_user == self._user_id))
            self.finish({'code':200,'msg':'取消关注成功'})
        except Exception as e:
            self.finish({'code':500,'msg':'取消关注失败'})


class FollowNumHandler(BaseHandler):
    @login_required_async
    async def post(self):
        # to 关注数
        # from  粉丝数
        type_ = self.get_body_argument('type_')
        if type_ == 'to':
            to_user = await manager.execute(FollowModel.select().where(FollowModel.from_user == self._user_id))
            self.finish({'code':200,'msg':'获取关注数成功','num':len(to_user._rows)})
        elif type_ == 'from':
            from_user = await manager.execute(FollowModel.select().where(FollowModel.to_user == self._user_id))
            self.finish({'code':200,'msg':'获取关注数成功','num':len(from_user._rows)})