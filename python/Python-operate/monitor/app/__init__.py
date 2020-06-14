# -*- coding: utf-8 -*-
import tornado.web  # web框架
import tornado.httpserver  # http服务
import tornado.ioloop  # 输入/输出事件循环
import tornado.options  # 配置工具

from tornado.options import options, define  # 选项、定义配置
from app.configs import configs  # 导入配置
from app.urls import urls  # 导入路由

# 定义一个服务的端口
define("port", default=8000, type=int, help="运行端口")


# 1.自定义应用
class CustomApplication(tornado.web.Application):
    # 重写__init__初始化构造方法
    def __init__(self):
        # 指定路由规则
        handlers = urls
        # 指定配置信息
        settings = configs
        # 调用父类__init__，传入这两个参数
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


# 2.自定义服务
def create_server():
    # 允许在命令行启动
    tornado.options.parse_command_line()
    # 创建http服务
    http_server = tornado.httpserver.HTTPServer(
        CustomApplication()
    )
    # 绑定监听端口
    http_server.listen(options.port)
    # 启动输入输出事件循环
    tornado.ioloop.IOLoop.instance().start()
