import tornado.web

from pycket.session import SessionMixin

from utils.photos import get_imgs, make_thumb
from utils.authentication import add_post_for, get_post_for, get_post


class AuthenHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('username')
        if current_user:
            return current_user
        return None


class IndexHandler(AuthenHandler):
    '''主页'''
    @tornado.web.authenticated  # 验证self.current_user 非None
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)
        print(posts[0].image_url)
        self.render('index.html', posts=posts)


class ExploreHandler(AuthenHandler):
    '''详情页'''
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)
        self.render('explore.html', posts=posts)


class PostHandler(tornado.web.RequestHandler):
    def get(self, post_id):
        post = get_post(post_id)
        if not post:
            self.render('error.html')
        else:
            self.render('post.html', post=post)


class UploadHandler(AuthenHandler):
    """
    上传图片的保存和展示，以及生成缩略图
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        # 获取form表单上传的name='newimg'文件的列表
        # 列表里的元素是格式为{"filename":..., "content_type":..., "body":...}的字典
        # filename 文件名, body 文件内容
        img_files = self.request.files.get('newimg', None)
        for img in img_files:
            img_url = 'uploads/{}'.format(img['filename'])
            save_to = './static/{}'.format(img_url)
            with open(save_to, 'wb') as f:
                f.write(img['body'])
            # 调用make_thumb方法，生成及保存缩略图
            thumb_url = make_thumb(save_to)

            user = self.current_user
            add_post_for(user, img_url, thumb_url)
            self.write("upload done......")