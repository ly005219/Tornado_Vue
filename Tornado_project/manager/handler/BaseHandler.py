from tornado.web import RequestHandler, Application



class BaseHandler(RequestHandler):
        def set_default_headers(self):
        # 设置默认的HTTP响应头
        # 'Access-Control-Allow-Origin' 头用于指定哪些网站可以访问该资源
        # '*' 表示允许所有来源访问
            self.set_header('Access-Control-Allow-Origin', '*')


       
                  

class MainHandler(RequestHandler):
    async def get(self):
        self.write("Hello, world")

