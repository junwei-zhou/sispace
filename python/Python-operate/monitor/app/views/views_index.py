# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.tools.monitor import Monitor
from app.tools.chart import Chart


# 定义一个首页视图
class IndexHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        m = Monitor()
        c = Chart()
        cpu_info = m.cpu()
        mem_info = m.mem()
        swap_info = m.swap()
        net_info = m.net()
        disk_info = m.disk()
        net_pie = [
            c.pie_two_html(
                "net{}".format(k + 1),
                "{}网卡信息".format(v["name"]),
                "收发包数统计",
                "收发字节统计",
                ["收包数", "发包数"],
                ["收字节", "发字节"],
                [v["packets_recv"], v["packets_sent"]],
                [v["bytes_recv"], v["bytes_sent"]],
            )
            for k, v in enumerate(net_info) if v["packets_recv"] and v['packets_sent']
        ]
        self.html("index.html",
                  data=dict(
                      title="系统监控",
                      cpu_info=cpu_info,
                      mem_info=mem_info,
                      swap_info=swap_info,
                      net_info=net_info,
                      disk_info=disk_info,
                      cpu_liquid=c.liquid_html("cpu_avg", "CPU平均使用率", cpu_info['percent_avg']),
                      mem_gauge=c.gauge_html("mem", "内存使用率", mem_info['percent']),
                      swap_gauge=c.gauge_html("swap", "交换分区使用率", mem_info['percent']),
                      net_pie=net_pie,
                  )
                  )
