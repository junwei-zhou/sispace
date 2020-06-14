# -*- coding:utf-8 -*-
import time
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler


class TestHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        time.sleep(5)
        self.write("<h1>hello world !</h1>")
