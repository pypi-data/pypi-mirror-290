#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time          : 2024-08-15
# @File          : LogUtil.py.py
# @Author        : XBW
# @Function      : 日志工具包
import os
import sys
import datetime
from loguru import logger


class BwLogings:
    __instance = None
    _is_logger_added = False  # 添加一个标志来检查是否已经添加了logger handler 防止重复添加

    # 文件名称，按天创建
    DATE = datetime.datetime.now().strftime('%Y-%m-%d')

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(BwLogings, cls).__new__(cls)
        return cls.__instance

    def __init__(self, logging_name=None, log_level="DEBUG", file_handler=True, log_dir=None, *args, **kwargs):
        if not self._is_logger_added:  # 只有当logger还没有添加handler时才执行添加
            if not file_handler:
                logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
                logger.add(sys.stderr,
                           level=log_level)  # 添加一个可以修改控制的handler
            else:
                os.makedirs(log_dir, exist_ok=True)
                if not logging_name:
                    logging_name = '%s/%s' % (log_dir, self.DATE)
                else:
                    logging_name = '%s/%s' % (log_dir, logging_name)

                self.logging_name = '%s.log' % logging_name

                logger.add(self.logging_name,
                           format="{time:YYYY-MM-DD HH:mm:ss}  | {level: <8} | {module}:{line} - {message}",
                           level=log_level,  # 设置日志等级
                           encoding='utf-8',
                           retention='30 days',  # 设置历史保留时长
                           backtrace=True,  # 回溯
                           diagnose=True,  # 诊断
                           enqueue=True)  # 异步写入

            self._is_logger_added = True  # 设置标志为True，表示已经添加了handler

    @property
    def logger(self):
        return logger


if __name__ == '__main__':
    logger = BwLogings(file_handler=False).logger


    def func(a, b):
        return a / b


    @logger.catch  # 线程或主线程中的异常捕获，它确保任何错误都正确地传播到日志记录器中
    def my(z, c):
        func(z, c)


    my(5, 0)
    logger.debug('bw nb')
