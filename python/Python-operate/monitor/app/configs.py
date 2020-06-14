# -*- coding: utf-8 -*-
import os  # 操作文件和目录

# 获取当前文件所在的目录
root_path = os.path.dirname(__file__)

# 配置文件
configs = dict(
    debug=True,  # 指定调试（开发者）模式：True；生产模式：False
    template_path=os.path.join(root_path, "templates"),
    static_path=os.path.join(root_path, "static")
)
