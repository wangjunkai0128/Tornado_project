import tornado.web
from utils.photos import get_imgs, make_thumb


class IndexHandler(tornado.web.RequestHandler):
    '''主页'''
    def get(self, *args, **kwargs):
        names = get_imgs("uploads")
        self.render('index.html', imgs=names)


class ExploreHandler(tornado.web.RequestHandler):
    '''详情页'''
    def get(self, *args, **kwargs):
        names = get_imgs("uploads/thumbnails")
        self.render('explore.html', imgs=names)


class PostHandler(tornado.web.RequestHandler):
    def get(self, post_id):
        self.render('post.html', post_id=post_id)


class UploadHandler(tornado.web.RequestHandler):
    """
    上传图片的保存和展示，以及生成缩略图
    """
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        # 获取form表单上传的name='newimg'文件的列表
        # 列表里的元素是格式为{"filename":..., "content_type":..., "body":...}的字典
        # filename 文件名, body 文件内容
        img_files = self.request.files.get('newimg', None)
        for img in img_files:
            save_to = './static/uploads/{}'.format(img['filename'])
            with open(save_to, 'wb') as f:
                f.write(img['body'])
            # 调用make_thumb方法，生成及保存缩略图
            make_thumb(save_to)
            self.write("upload done......")