"""
SQLAlchemy，连接数据库
"""
# 导入create_engine模块
from sqlalchemy import create_engine

# 数据库数据
HOST = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'qwe123'
DATABASE = 'tornado_project'

# 数据库URL
Db_url = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
    DATABASE
)

# 实例化
engine = create_engine(Db_url)
# engine = create_engine("mysql+pymysql://root:qwe123@127.0.0.1:3306/Mydb?charset=utf8")

# 创建一个基类
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(engine)

# 创建会话
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)
session = Session()

# 测试连接数据库
if __name__ == "__main__":
    connection = engine.connect()
    result = connection.execute("select 1")
    print(result.fetchone())

