import mysql.connector
from sqlalchemy import create_engine  # 创建引擎
from sqlalchemy.orm import sessionmaker  # 创建会话


class ORM:
    # 会话方法
    @classmethod
    def db(cls):
        mysql_configs = dict(
            db_host="127.0.0.1",  # 主机地址
            db_name="monitor",  # 数据库名称
            db_port=3306,  # 数据库端口
            db_user="root",  # 数据库用户
            db_pwd=""  # 数据库密码
        )
        link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8".format(
            **mysql_configs
        )
        # 创建引擎
        engine = create_engine(
            link,
            encoding="utf-8",
            echo=False,
            pool_size=100,
            pool_recycle=10,
            connect_args={'charset': 'utf8'}
        )
        # 创建会话
        Session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )
        return Session()
