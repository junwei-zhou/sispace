# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base  # 模型继承父类
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, DATE, TIME, DATETIME  # 导入字段
from sqlalchemy import Column  # 创建字段

Base = declarative_base()  # 调用
metadata = Base.metadata  # 创建元类
"""
1.导入模型继承父类
2.导入数据类型
3.导入创建字段的类
4.定义模型
"""


# 内存统计
class Mem(Base):
    __tablename__ = "mem"  # 指定表名称
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


# 交换分区统计
class Swap(Base):
    __tablename__ = "swap"  # 指定表名称
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


# CPU统计
class Cpu(Base):
    __tablename__ = "cpu"  # 指定表名称
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


if __name__ == "__main__":
    # 1.导入数据库连接驱动
    import mysql.connector
    # 2.导入创建引擎
    from sqlalchemy import create_engine

    # 配置一下连接信息
    mysql_configs = dict(
        db_host="127.0.0.1",  # 主机地址
        db_name="monitor",  # 数据库名称
        db_port=3306,  # 数据库端口
        db_user="root",  # 数据库用户
        db_pwd=""  # 数据库密码
    )

    """
    连接格式：mysql+驱动名称://用户:密码@主机:端口/数据库名称
    """
    link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(
        **mysql_configs
    )

    # 创建连接引擎，encoding定义编码，echo是(True)否(False)输出日志
    engine = create_engine(link, encoding="utf-8", echo=True)

    # 映射
    metadata.create_all(engine)
