import functools
import jwt

from config import secret, jwt_exp
from manager import manager
from manager.models import User

def login_required_async(func):
    @functools.wraps(func)
    async def wrapper(self,*arg,**kwargs):
        # 验证用户是否登录
        # 获取token
        token = self.request.headers.get('token')
        # 从token值中解析出email
        payload = jwt.decode(token, secret,options={'verify_exp':True},algorithms=["HS256"],leeway=jwt_exp)
        if payload:
            # 通过email查询数据
            email = payload.get('email')
            try:
                user = await manager.get(User,email = email)


            
                self._user_email = email
                self._user_id = user.id
                # 登录了,运行func()
                await func(self,*arg,**kwargs)
            except Exception as e:
                print(e)
                self.finish({'msg':'请先登录','code':401})
        else:
            # 没有登录,回馈请登录
            self.finish({'msg':'请先登录','code':401})
    return wrapper