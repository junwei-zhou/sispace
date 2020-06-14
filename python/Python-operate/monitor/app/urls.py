# -*- coding: utf-8 -*-
from sockjs.tornado import SockJSRouter  # 定义路由的
from app.views.views_index import IndexHandler as index  # 导入系统监控视图
from app.views.views_log import LogHandler as log  # 导入日志监控视图
from app.views.views_real_time import RealTimeHandler as real_time
from app.views.views_test import TestHandler as test

# 配置路由视图映射规则
urls = [
           (r"/", index),
           (r"/test/", test),
           (r"/log/", log),
       ] + SockJSRouter(real_time, "/real/time").urls
