import tornado.web
from .main import AuthenHandler
from utils.authentication import authen, register


class LoginHandler(AuthenHandler):
    """
    登录接口
    """
    def get(self, *args, **kwargs):
        nextname = self.get_argument('next', None)
        self.render('login.html', nextname=nextname)

    def post(self, *args, **kwargs):
        nextname = self.get_argument('next', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        passed = authen(username, password)
        if passed:
            self.session.set('username', username)
            self.redirect(nextname)
        else:
            self.write('登录失败......用户名或密码错误！')


class LogoutHandler(AuthenHandler):
    '''登出接口'''
    def get(self, *args, **kwargs):
        self.session.set('username', '')
        self.redirect('/')

    def post(self, *args, **kwargs):
        if (self.get_argument('logout', None)):
            # delete的是服务器端的session数据，客户端体现不出来
            self.session.delete('username')
        self.redirect('/')


class RegisterHandler(AuthenHandler):
    def get(self, *args, **kwargs):
        self.render('register.html', msg='')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)

        if username and password1 and password2:
            if password1 != password2:
                self.render('register.html', msg='您两次输入的密码不匹配，请重新输入......')
            else:
                ret = register(username, password1)
                if ret['msg'] == 'ok':
                    self.redirect('/')
                else:
                    self.write(ret['msg'])
        else:
            self.render('register.html', msg='注册失败，请重新注册！')



