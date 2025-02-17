from tornado.web import RequestHandler
from manager.wtforms import *
from manager.models import User
from manager import manager
from uuid import uuid4
from manager.handler.BaseHandler import BaseHandler
from manager.utils.email_util import send_mail
from random import randint
from config import email
from manager.utils.redis_utils import save_code,get_code
import jwt
from config import secret,settings

class AddUserHandler(BaseHandler):
    async def post(self):
        #创建一个响应对象
        rs_data={}
        user_form=UserForm(self.request.arguments)
        code=self.get_body_argument('code')
        #验证验证码
        db_code= get_code(user_form.email.data)
        if not db_code or code!=db_code:
            rs_data['code']=500
            rs_data['msg']='验证码错误'
            self.finish(rs_data)
          
        if user_form.validate():
            #保存数据
            #验证邮箱是否注册
            email=user_form.email.data#前端提交的邮箱
            try:
                exit_email= await manager.get(User,User.email==email)
                if exit_email:#存在
                    #存在
                    rs_data['code']=500
                    rs_data['msg']='邮箱已注册'
            except Exception as e:
                #不存在

                user_form.id.data=uuid4()
                await manager.create(User,**user_form.data)
                #返回响应
                rs_data['code']=200
                rs_data['msg']='注册成功'

        else:
            #显示错误信息
            rs_data['code']=500
            rs_data['msg']='注册失败'
            for f in user_form.errors:
                rs_data[f]=user_form.errors[f][0]
        self.finish(rs_data)

class SendEmailHandler(BaseHandler):
    def generate_code(self) ->int:
        # random.randint(1000,9999)
        # random.choice('0123456789')
        return randint(1000,9999)

    def post(self):
        #获取前端提交的邮箱
        user_email = self.get_body_argument('email')
        code= self.generate_code()
        msg = f'您好，您正在使用{user_email}注册<LY-CMS项目>用户注册账号，您的验证为{code},如果不是本人操作请忽略此邮件！'
        send_mail(email.get('host'),email.get('pwd'),user_email,'<LY-CMS项目>用户注册',msg)
        save_code(user_email,code)
        

class LoginHandler(BaseHandler):
    async def post(self):
        rs_data = {}
        user_form = LoginUserForm(self.request.arguments)
        if user_form.validate():
            # 验证成功
            # 从获取数据库中获取用户信息
            try:
                user =  await manager.get(User,email = user_form.email.data ,password = user_form.password.data)
                


                # 获取到了,登录成功
                rs_data['code']= 200
                rs_data['msg'] = '登录成功!'
                # 生成一个用户信息(加密),返回给前端.下一次访问时,携带用户信息回来即可
                payload ={
                    'email':user_form.email.data
                }
                token = jwt.encode(payload,secret,algorithm="HS256") # 要加密的数据,加密的密码,加密的算法
                rs_data['token'] = token
            except Exception as e:
                print(e)
                # 获取不到,登录失败
                rs_data['code']= 401
                rs_data['msg'] = '用户名或密码错误'
        else:
            rs_data['code']= 401
            rs_data['msg'] = '用户名不符合规范'
            for f in user_form.errors:
                rs_data[f] = user_form.errors[f][0]
        
        self.finish(rs_data)



# class GetUserHandler(BaseHandler):
#     async def get(self):
#         rs_data = {}
#         # 获取token
#         token = self.request.headers.get('token')
#         # 从token值中解析出email
#         payload = jwt.decode(token, secret, algorithms=["HS256"])
#         if payload:
#             # 通过email查询数据
#             email = payload.get('email')
#             user = await manager.get(User,email = email)
#             # 判断是否查到数据
#             if user:
#             # 有数据,将用户信息返回给前端
#                 rs_data['code'] = 200
#                 rs_data['msg'] = '获取用户成功!'
#                 rs_data['user'] = user.to_json()
#             # 没有数据,没有登录
#             else:
#                 rs_data['code'] = 500
#                 rs_data['msg'] = 'token错误!' 
#         # 没有email,就是登录
#         else:
#             rs_data['code'] = 500
#             rs_data['msg'] = '请登录后再操作'
#         self.finish(rs_data)

from manager.decorators import login_required_async





class GetUserHandler(BaseHandler):
    @login_required_async
    async def get(self):
        rs_data = {}
        id  = self._user_id
        try:
            user = await manager.get(User,id = id)
            # 判断是否查到数据
            if user:
            # 有数据,将用户信息返回给前端
                rs_data['code'] = 200
                rs_data['msg'] = '获取用户成功!'
                rs_data['user'] = user.to_json()           
        except Exception as e:
            rs_data['code'] = 500
            rs_data['msg'] = '获取用户信息错误!' 

        self.finish(rs_data)

import os
#更新
class UpdateUserHandler(BaseHandler):
    async def post(self):
        rs_data ={}
        user_form = UpdateUserForm(self.request.arguments)
        if user_form.validate():
            id = user_form.id.data
            # id email password
            user_form.email.data = user_form.email.data.strip() # 因为前端传递来的数据前后有空格，所以去掉空格，避免修改登录账号
           
            # 获取头像文件数据
            pic = self.request.files.get('pic',[{}])[0]
            # 因为有多位用户上传头像，为避免图像的文件名重复，所以随机生成一个名字
            file_name = uuid4().hex
            # 获取原文件的后缀名
            file_suffix = os.path.splitext(pic.get('filename'))[-1]
            full_name = file_name + file_suffix

            # 为了保证用户可以访问到自己上传的头像，因此要把头像上传到静态文件夹
            full_path = os.path.join(settings.get('static_path'),'img',full_name)
            # 保存头像
            with open(full_path,'wb') as f:
                f.write(pic.get('body'))
            print(full_path)
            # 更新用户的头像地址 /static/img/xxx.png
            user_form.pic.data = os.path.join('/static/img',full_name)
            rs = await manager.execute(User.update(**user_form.data).where(User.id == id))
            if rs > 0 :
                rs_data['code'] = 200
                rs_data['msg'] = '更新用户信息成功！'
            else:
                rs_data['code'] = 500
                rs_data['msg'] = '更新用户信息失败！'
        else:
            rs_data['code'] = 500
            rs_data['msg'] = '数据不合法!'

        self.finish(rs_data)