from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table
from .connect import Base, session
from sqlalchemy import ForeignKey
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship


# 定义Models
class Users(Base):
    # 表名是固定写法 __tablename__
    __tablename__ = 'users'
    # Column 创建字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)
    creatime = Column(DateTime, default=datetime.now)
    _locked = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return """ <User(id:%s, username:%s, password:%s, creatime:%s, _locked:%s)> """ % (
            self.id,
            self.username,
            self.password,
            self.creatime,
            self._locked
        )

    @classmethod
    def is_exists(cls, username):
        # 引用exists方法要先导入 from sqlalchemy.sql import exists
        # exists().where(cls.username == username)).scalar()存在username就返回Ture，否则返回False
        result = session.query(exists().where(cls.username == username)).scalar()
        return result

    @classmethod
    def add_user(cls, username, password):
        # 添加用户和密码到数据库
        user = cls(username=username, password=password)

        session.add(user)
        session.commit()

    @classmethod
    def get_pass(cls, username):
        # 通过用户名查找数据库里面对应的用户名的密码
        user = session.query(cls).filter_by(username=username).first()
        if user:
            return user.password
        return ''


class Posts(Base):
    """
    用户图片信息存储表
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(80))
    thumb_url = Column(String(80))

    # user_id是users表id字段的外键
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', backref='posts', uselist=False, cascade='all')

    def __repr__(self):
        return """<Post(id:%s, image_url:%s, thumb_url:%s)>""" % (
            self.id,
            self.image_url,
            self.thumb_url
        )


if __name__ == "__main__":
    # 创建表，需要执行这行代码。如果表存在，则不会更改
    Base.metadata.create_all()
