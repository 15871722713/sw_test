# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-23 09:47:55
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-06 12:40:26

import os
import time

LOG_LEVEL = 1
DEBUG = 1


def set_log_level(level):
    global LOG_LEVEL
    LOG_LEVEL = level


def logfile(file):
    global fs
    fs = open(file, 'w')


def log(msg):
    fs.write(msg + '\n')
    fs.flush()
    print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + msg)


def debug(msg):
    global LOG_LEVEL
    global DEBUG
    if LOG_LEVEL <= DEBUG:
        print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + msg)


def close_log_file():
    fs.close()
