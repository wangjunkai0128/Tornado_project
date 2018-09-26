import os
import glob
from PIL import Image

def get_imgs(path):
    """
    获取static路径path目录下所有.jpg格式的文件
    :param path:
    :return:
    """
    # 切换到 app.py主程序所在的路径下的 static目录
    os.chdir("static/")
    # 获取path目录下的所有jpg文件
    names = glob.glob("{}/*.jpg".format(path))
    # 切换到上一级目录
    os.chdir("..")

    return names

def make_thumb(path):
    """
    生成缩略图，并保存到thumbnails目录
    :param path:
    :return:
    """
    # 获取path路径下，文件的相对路径
    dirname = os.path.dirname(path)
    # 获取文件
    filename = os.path.basename(path)
    # 分离文件名和文件后缀
    file, ext = os.path.splitext(filename)
    # 实例化图片对象
    im = Image.open(path)
    size = (128, 128)
    # 图片缩放尺寸
    im.thumbnail(size)
    # 文件保存路径
    save_thumb_to = os.path.join(dirname, 'thumbnails', '{}_{}x{}.jpg'.format(file, *size))
    im.save(save_thumb_to, 'JPEG')
    thumb_url = os.path.relpath(save_thumb_to, 'static')
    return thumb_url

