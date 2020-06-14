# -*- coding: utf-8 -*-
import datetime
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from sqlalchemy import and_, func  # 并列条件连接符
from app.tools.orm import ORM  # 导入会话类
from app.models.models import Mem, Swap, Cpu  # 导入硬件信息模型
from app.tools.chart import Chart


class LogHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        # 用id参数来标识
        id = self.get_argument("id", 1)
        data = dict(title="日志统计")
        c = Chart()
        # id = 1表示1小时内
        if int(id) == 1:
            attr_cpu, attr_mem, attr_swap, vals_cpu, vals_mem, vals_swap = self.data_by_hour()
            # 内存折线面积图
            if attr_mem and vals_mem:
                data["line_mem"] = c.line_html(
                    "内存使用率日志[1小时内]",
                    attr_mem,
                    vals_mem,
                    "red"
                )
            else:
                data["line_mem"] = "<div class='alert alert-danger'>没有内存[1小时内]数据</div>"

            # 交换分区折线面积图
            if attr_swap and vals_swap:
                data["line_swap"] = c.line_html(
                    "交换分区使用率日志[1小时内]",
                    attr_swap,
                    vals_swap,
                    "blue"
                )
            else:
                data["line_swap"] = "<div class='alert alert-danger'>没有交换分区[1小时内]数据</div>"

            # CPU折线面积图
            if attr_cpu and vals_cpu:
                data["line_cpu"] = c.line_html(
                    "CPU使用率日志[1小时内]",
                    attr_cpu,
                    vals_cpu,
                    "green"
                )
            else:
                data["line_cpu"] = "<div class='alert alert-danger'>没有CPU[1小时内]数据</div>"

        # id = 2表示1天内
        if int(id) == 2:
            attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg, \
            attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg, \
            attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg = self.data_by_three()
            if attr_mem and vals_mem_min and vals_mem_max and vals_mem_avg:
                data['line_mem'] = c.line_three_html(
                    "内存使用率日志[今天]",
                    attr_mem,
                    vals_mem_min,
                    vals_mem_max,
                    vals_mem_avg
                )
            else:
                data["line_mem"] = "<div class='alert alert-danger'>没有内存[今天]数据</div>"
            if attr_swap and vals_swap_min and vals_swap_max and vals_swap_avg:
                data['line_swap'] = c.line_three_html(
                    "交换分区使用率日志[今天]",
                    attr_swap,
                    vals_swap_min,
                    vals_swap_max,
                    vals_swap_avg
                )
            else:
                data["line_swap"] = "<div class='alert alert-danger'>没有交换分区[今天]数据</div>"
            if attr_cpu and vals_cpu_min and vals_cpu_max and vals_cpu_avg:
                data['line_cpu'] = c.line_three_html(
                    "CPU使用率日志[今天]",
                    attr_cpu,
                    vals_cpu_min,
                    vals_cpu_max,
                    vals_cpu_avg
                )
            else:
                data["line_cpu"] = "<div class='alert alert-danger'>没有CPU[今天]数据</div>"
        # id = 3表示1个月内
        if int(id) == 3:
            attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg, \
            attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg, \
            attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg = self.data_by_three(
                method="month",
                format="%Y%m%d"
            )
            if attr_mem and vals_mem_min and vals_mem_max and vals_mem_avg:
                data['line_mem'] = c.line_three_html(
                    "内存使用率日志[本月]",
                    attr_mem,
                    vals_mem_min,
                    vals_mem_max,
                    vals_mem_avg
                )
            else:
                data["line_mem"] = "<div class='alert alert-danger'>没有内存[本月]数据</div>"
            if attr_swap and vals_swap_min and vals_swap_max and vals_swap_avg:
                data['line_swap'] = c.line_three_html(
                    "交换分区使用率日志[本月]",
                    attr_swap,
                    vals_swap_min,
                    vals_swap_max,
                    vals_swap_avg
                )
            else:
                data["line_swap"] = "<div class='alert alert-danger'>没有交换分区[本月]数据</div>"
            if attr_cpu and vals_cpu_min and vals_cpu_max and vals_cpu_avg:
                data['line_cpu'] = c.line_three_html(
                    "CPU使用率日志[本月]",
                    attr_cpu,
                    vals_cpu_min,
                    vals_cpu_max,
                    vals_cpu_avg
                )
            else:
                data["line_cpu"] = "<div class='alert alert-danger'>没有CPU[本月]数据</div>"
        self.html("log.html", data=data)

    # 一小时内数据查询方法
    def data_by_hour(self):
        now_time, next_time = self.dt_range()
        attr_cpu, attr_mem, attr_swap = None, None, None  # 属性
        vals_cpu, vals_mem, vals_swap = None, None, None  # 值
        session = ORM.db()  # 创建会话
        try:
            # 执行代码块
            # 内存
            mem = self.one_hour_query(Mem, session, now_time, next_time)
            if mem:
                attr_mem = [v.create_time.strftime("%H:%M:%S") for v in mem]
                vals_mem = [float(v.percent) for v in mem]

            # 交换分区
            swap = self.one_hour_query(Swap, session, now_time, next_time)
            if swap:
                attr_swap = [v.create_time.strftime("%H:%M:%S") for v in swap]
                vals_swap = [float(v.percent) for v in swap]

            # CPU
            cpu = self.one_hour_query(Cpu, session, now_time, next_time)
            if cpu:
                attr_cpu = [v.create_time.strftime("%H:%M:%S") for v in cpu]
                vals_cpu = [float(v.percent) for v in cpu]

        except Exception as e:
            # 发生异常
            session.rollback()  # 回滚
        else:
            # 没有发生异常
            session.commit()  # 提交会话
        finally:
            # 无论是否发生异常都要执行
            session.close()  # 关闭会话

        return attr_cpu, attr_mem, attr_swap, vals_cpu, vals_mem, vals_swap

    # 一小时查询方法
    def one_hour_query(self, model, session, now_time, next_time):
        """
        model：模型（Cpu、Mem、Swap）
        order_by：排序（按时间升序排序）
        filter：过滤条件（时间大于等于当前时间0分0秒，小于下1个小时的0分0秒）
        """
        data = session.query(model).order_by(model.create_dt.asc()).filter(
            and_(
                model.create_dt >= now_time.strftime("%Y-%m-%d %H") + ":00:00",
                model.create_dt < next_time.strftime("%Y-%m-%d %H") + ":00:00",
            )
        ).all()
        return data

    # 查询三种曲线数据
    def data_by_three(self, method="day", format="%Y%m%d%H"):
        session = ORM.db()
        attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg = None, None, None, None
        attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg = None, None, None, None
        attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg = None, None, None, None
        try:
            # 内存
            mem = self.three_query(Mem, session, method, format)
            if mem:
                attr_mem = [v[0] for v in mem]
                vals_mem_min = [float(v[1]) for v in mem]
                vals_mem_max = [float(v[2]) for v in mem]
                vals_mem_avg = [round(float(v[3]), 1) for v in mem]
            # 交换分区
            swap = self.three_query(Swap, session, method, format)
            if swap:
                attr_swap = [v[0] for v in swap]
                vals_swap_min = [float(v[1]) for v in swap]
                vals_swap_max = [float(v[2]) for v in swap]
                vals_swap_avg = [round(float(v[3]), 1) for v in swap]
            # CPU
            cpu = self.three_query(Cpu, session, method, format)
            if cpu:
                attr_cpu = [v[0] for v in cpu]
                vals_cpu_min = [float(v[1]) for v in cpu]
                vals_cpu_max = [float(v[2]) for v in cpu]
                vals_cpu_avg = [round(float(v[3]), 1) for v in cpu]
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg, \
               attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg, \
               attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg

    # 查询最大值，最小值，平均值方法
    def three_query(self, model, session, method="day", format="%Y%m%d%H"):
        """
        func.date_format(model.create_dt, format)转化日期格式，把第1个参数转化为format格式
        """
        model_query = session.query(
            func.date_format(model.create_dt, format),
            func.min(model.percent),
            func.max(model.percent),
            func.avg(model.percent)
        )
        data = None
        if method == "day":
            # 过滤出今天的数据
            # 按照小时分组
            # 按照时间升序排序
            data = model_query.filter(
                func.to_days(model.create_dt) == func.to_days(func.now())
            ).group_by(
                func.date_format(model.create_dt, format)
            ).order_by(model.create_dt.asc()).all()
        if method == "month":
            # 过滤出当前月的数据
            # 按照天来分组
            # 按照时间升序排序
            data = model_query.filter(
                func.date_format(model.create_dt, "%Y%m") == func.date_format(func.curdate(), "%Y%m")
            ).group_by(
                model.create_date
            ).order_by(model.create_dt.asc()).all()
        return data

    # 时间范围方法
    def dt_range(self):
        now_time = datetime.datetime.now()  # 当前小时的时间
        next_time = now_time + datetime.timedelta(hours=1)  # 下一个小时时间
        return now_time, next_time
