import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from handlers import main, authen


define('port', default=8000, help='About port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
            ('/upload', main.UploadHandler),
            ('/register', authen.RegisterHandler),
            ('/login', authen.LoginHandler),
            ('/logout', authen.LogoutHandler),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            # 如果加了验证登录装饰器，login_url就是验证没有登录时跳转到的页面
            login_url='/login',
            cookie_secret='wangjunkai',
            pycket={
                    'engine': 'redis',
                    'stroage': {
                        'host': '192.168.83.128',
                        'port': '6379',
                        # 指定数据库
                        'db_sessions': 5,
                        'db_notifications': 11,
                        'max_connections': 2 ** 31,
                    },
                    'cookies': {
                        'expires_days': 30,
                        # 'max_age': 200
                         }
                },
        )
        super(Application, self).__init__(handlers, **settings)


application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
