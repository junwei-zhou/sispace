# -*- coding: utf-8 -*-
import psutil
import time
import datetime
from pprint import pprint  # 格式化打印（美化输出工具）


# 定义一个专门用于获取系统信息的类

class Monitor(object):
    # 专门用于单位转化的方法
    def bytes_to_gb(self, data, key=""):
        if key == "percent":
            return data
        else:
            return round(data / (1024 ** 3), 2)

    # 专门获取CPU信息
    def cpu(self):
        # percpu：True获取每个CPU的使用率，False获取平均使用率
        # 1.平均、2.单独、3.物理CPU核心数、4.逻辑CPU核心数
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),
            percent_per=psutil.cpu_percent(interval=0, percpu=True),
            num_p=psutil.cpu_count(logical=False),
            num_l=psutil.cpu_count(logical=True)
        )
        return data

    # 专门获取内存信息
    def mem(self):
        # 内存信息
        info = psutil.virtual_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),
            used=self.bytes_to_gb(info.used),
            free=self.bytes_to_gb(info.free),
            percent=info.percent
        )
        return data

    # 专门获取交换分区/文件信息
    def swap(self):
        # 交换文件/分区信息
        info = psutil.swap_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),
            free=self.bytes_to_gb(info.free),
            used=self.bytes_to_gb(info.used),
            percent=info.percent
        )
        return data

    # 专门获取磁盘信息
    def disk(self):
        # 专门获取磁盘分区信息
        info = psutil.disk_partitions()
        # 列表推导式
        data = [
            dict(
                device=v.device,
                mountpoint=v.mountpoint,
                fstype=v.fstype,
                opts=v.opts,
                used={
                    k: self.bytes_to_gb(v, k)
                    for k, v in psutil.disk_usage(v.mountpoint)._asdict().items()
                }
            )
            for v in info
        ]
        return data

    # 专门获取网络信息
    def net(self):
        # 获取地址信息
        addrs = psutil.net_if_addrs()
        # val.family.name取出协议地址族名称，AF_INET
        addrs_info = {
            k: [
                dict(
                    family=val.family.name,
                    address=val.address,
                    netmask=val.netmask,
                    broadcast=val.broadcast
                )
                for val in v if val.family.name == "AF_INET"
            ][0]
            for k, v in addrs.items()
        }
        # 获取输入输出信息（收发包数，收发字节数）
        io = psutil.net_io_counters(pernic=True)
        data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **addrs_info[k]
            )
            for k, v in io.items()
        ]
        return data

    # 时间戳转化为时间字符方法
    def td(self, tm):
        dt = datetime.datetime.fromtimestamp(tm)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 获取日期时间
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 专门获取最近开机时间
    def lastest_start_time(self):
        # 时间戳
        return self.td(psutil.boot_time())

    # 专门获取系统登录用户
    def logined_users(self):
        users = psutil.users()
        data = [
            dict(
                name=v.name,
                terminal=v.terminal,
                host=v.host,
                started=self.td(v.started),
                pid=v.pid
            )
            for v in users
        ]
        return data


if __name__ == "__main__":
    m = Monitor()
    """
    for v in range(1, 11):
        print(m.cpu())
        time.sleep(1)  # 每隔一秒打印一次
    """
    # print(m.mem())
    # print(m.swap())
    # pprint(m.disk())
    pprint(m.logined_users())
