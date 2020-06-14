# -*- coding: utf-8 -*-
import time
import datetime
from app.models.models import Cpu, Mem, Swap
from app.tools.monitor import Monitor
from app.tools.orm import ORM


# 日期时间函数
def dt():
    now = datetime.datetime.now()
    _date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    _date = now.strftime("%Y-%m-%d")
    _time = now.strftime("%H:%M:%S")
    return _date, _time, _date_time


# 定义保存日志的函数
def save_log():
    m = Monitor()
    cpu_info, mem_info, swap_info = m.cpu(), m.mem(), m.swap()
    _date, _time, _date_time = dt()
    # 1.创建会话
    session = ORM.db()
    try:
        # CPU
        cpu = Cpu(
            percent=cpu_info["percent_avg"],
            create_date=_date,
            create_time=_time,
            create_dt=_date_time
        )
        # 内存
        mem = Mem(
            percent=mem_info['percent'],
            total=mem_info['total'],
            used=mem_info['used'],
            free=mem_info['free'],
            create_date=_date,
            create_time=_time,
            create_dt=_date_time
        )
        # 交换分区
        swap = Swap(
            percent=swap_info['percent'],
            total=swap_info['total'],
            used=swap_info['used'],
            free=swap_info['free'],
            create_date=_date,
            create_time=_time,
            create_dt=_date_time
        )
        # 提交至数据块
        session.add(cpu)
        session.add(mem)
        session.add(swap)
    except Exception as e:
        session.rollback()  # 如果发送异常回滚
    else:
        session.commit()  # 没有异常提交
    finally:
        session.close()  # 无论是否发生异常关闭


if __name__ == "__main__":
    while True:
        _date, _time, _date_time = dt()
        print("开始时间：{}".format(_date_time))
        save_log()
        print("结束时间：{}".format(_date_time))
        time.sleep(5)  # 每隔5秒采集一次
