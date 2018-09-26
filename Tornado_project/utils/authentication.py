import hashlib

from models.user_models import Users, Posts
from models.connect import session


def hashlib_md5(password):
    # 给需要加密的参数加密，这里是给密码加密
    return hashlib.md5(password.encode('utf8')).hexdigest()

def authen(username, password):
    """
    验证用户名和密码是否与保存的相匹配
    :param username:
    :param password:
    :return:
    """
    if username and password:
        user_password = Users.get_pass(username)
        return (hashlib_md5(password) == user_password)
    else:
        return False

def register(username, password):
    """
    检验用户名是否存在并保存到数据库
    :param username:
    :param password:
    :return:
    """
    if Users.is_exists(username):
        return {'msg': '用户名已经存在，请重新注册......'}

    hash_pass = hashlib_md5(password)
    Users.add_user(username, hash_pass)
    return {'msg': 'ok'}

def add_post_for(username, img_url, thumb_url):
    """
    保存用户上传的图片信息到数据库
    :param username:
    :param img_url:
    :param thumb_url:
    :return:
    """
    user = session.query(Users).filter_by(username=username).first()
    post = Posts(image_url=img_url, thumb_url=thumb_url, user=user)

    session.add(post)
    session.commit()

def get_post_for(username):
    """
    获取某个用户上传的图片信息
    :param username:
    :return:
    """
    user = session.query(Users).filter_by(username=username).first()
    if user:
        return user.posts
    else:
        return []

def get_post(post_id):
    post = session.query(Posts).filter_by(id=post_id).first()
    return post