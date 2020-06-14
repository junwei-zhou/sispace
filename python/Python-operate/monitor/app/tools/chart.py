# -*- coding: utf-8 -*-
import datetime
from pyecharts import Liquid, Gauge, Pie, Line


class Chart(object):
    # 水球图
    def liquid_html(self, chart_id, title, val):
        # 基本配置
        liquid = Liquid(
            "{}-{}".format(
                self.dt, title
            ),
            title_pos="center",
            width="100%",
            title_color="white",
            title_text_size=14,
            height=300
        )
        # 绑定id
        liquid.chart_id = chart_id
        # 添加参数
        liquid.add("", [round(val / 100, 4)])
        return liquid.render_embed()  # 返回图表html代码

    # 仪表图
    def gauge_html(self, chart_id, title, val):
        gauge = Gauge(
            "{}-{}".format(self.dt, title),
            title_pos="center",
            width="100%",
            title_text_size=14,
            title_color="white",
            height=300
        )
        gauge.chart_id = chart_id
        gauge.add(
            "",
            "",
            val,
            scale_range=[0, 100],
            is_legend_show=False
        )
        return gauge.render_embed()

    # 饼状图
    def pie_two_html(self, chart_id, title, sub_title1, sub_title2, key1, key2, val1, val2):
        # 实例化饼状图
        pie = Pie(
            "{}-{}".format(self.dt, title),
            title_pos="center",
            width="100%",
            height=300,
            title_text_size=14,
            title_color="white"
        )
        # 指定ID
        pie.chart_id = chart_id
        # 绑定属性和值
        pie.add(
            sub_title1,
            key1,
            val1,
            center=[25, 50],
            is_random=True,
            radius=[30, 75],
            rosetype="area",
            is_legend_show=False,
            is_label_show=True
        )
        pie.add(
            sub_title2,
            key2,
            val2,
            center=[75, 50],
            is_random=True,
            radius=[30, 75],
            rosetype="area",
            is_legend_show=False,
            is_label_show=True
        )
        return pie.render_embed()

    # 折线面积图
    def line_html(self, title, key, val, color=None):
        line = Line(
            title,
            title_pos="center",
            width="100%",
            height=300
        )
        line.add(
            "",
            key,
            val,
            mark_point=["average", "max", "min"],
            mark_line=["average", "max", "min"],
            area_color=color,
            line_opacity=0.2,
            area_opacity=0.4,
            is_datazoom_show=True,
            datazoom_range=[0, 100],
            symbol=None
        )
        return line.render_embed()

    # 折线面积图
    def line_three_html(self, title, key, val_min, val_max, val_avg):
        line = Line(
            title,
            title_pos="left",
            width="100%",
            height=300
        )
        line.add(
            "最小值",
            key,
            val_min,
            mark_point=["average", "max", "min"],
            is_datazoom_show=True,
            datazoom_range=[0, 100],
            is_smooth=True
        )
        line.add(
            "最大值",
            key,
            val_max,
            mark_point=["average", "max", "min"],
            is_datazoom_show=True,
            datazoom_range=[0, 100],
            is_smooth=True
        )
        line.add(
            "平均值",
            key,
            val_avg,
            mark_point=["average", "max", "min"],
            is_datazoom_show=True,
            datazoom_range=[0, 100],
            is_smooth=True
        )
        return line.render_embed()

    # 日期时间方法
    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
