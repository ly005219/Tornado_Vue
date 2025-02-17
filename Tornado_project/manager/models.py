
from peewee import *
from manager import db
from datetime import datetime

class BaseModel(Model):
    create_time=DateTimeField(default=datetime.now,verbose_name='创建时间')

    def to_json(self):
            # 初始化一个空字典r，用于存储转换后的JSON数据
             r={}
            # 遍历self.__data__字典中的所有键
             for k in self.__data__.keys():
                # 如果键是'create_time'
                if k=='create_time':
                    # 将'create_time'的值转换为字符串格式，并存储到字典r中
                      r[k]=str(getattr(self,k))
                # 对于其他键
                else:
                    # 直接将键对应的值存储到字典r中
                  r[k]=getattr(self,k)
             # 返回字典r
             return r

    class Meta:
        database=db


class User(BaseModel):
    id=CharField(primary_key=True)
    email=CharField(max_length=32,verbose_name='邮箱')
    nick_name=CharField(max_length=32,verbose_name='昵称',null=True)
    gender=IntegerField(verbose_name='性别',null=True)
    password=CharField(max_length=32,verbose_name='密码')
    signatrue=CharField(max_length=100,verbose_name='签名',null=True)
    pic=CharField(max_length=100,verbose_name='头像',null=True)
    status=IntegerField(default=1,verbose_name='状态')

    class Meta:
        table_name='t_user'


class TopicModel(BaseModel):
    id =  CharField(primary_key=True)
    title = CharField(verbose_name='标题')
    imgs =  CharField(max_length=1000,verbose_name='图片')
    content =  CharField(verbose_name='内容')
    chick_num =  IntegerField(verbose_name='点击数')
    type_ =  CharField(verbose_name='类型')
    user =  ForeignKeyField(User,backref='topics')

    class Meta:
        table_name = 't_topic'


class CommentModel(BaseModel):
    id = CharField(primary_key = True)
    content = CharField(verbose_name='内容')
    topic = ForeignKeyField(TopicModel,backref='comments')
    user = ForeignKeyField(User,backref='comments')

    class Meta:
        table_name = 't_comment'


# 用户  帖子
# 1位用户  收藏多个帖子
# 1个帖子  可以被多位用户收藏

class CollectionModel(BaseModel):
    topic = ForeignKeyField(TopicModel,backref='collections')
    user = ForeignKeyField(User,backref='collections')

    class Meta:
        table_name = 't_collection'
        primary_key =CompositeKey('topic','user')


# 用户 关注 用户
# 1位用户 可以关注  多位用户
# 1位用户 可以被关注  多位用户
# zs -> ls ww
# ls -> zs ww
# ww -> zs ls
# 自关联的多对多关系

class FollowModel(BaseModel):
    to_user = ForeignKeyField(User,backref='to_user')
    from_user = ForeignKeyField(User,backref='from_user')

    class Meta:
        table_name = 't_follow'
        primary_key = CompositeKey('to_user','from_user')