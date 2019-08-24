# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-24 20:44:58
# @Last Modified by:   JinHua
# @Last Modified time: 2019-08-24 21:50:22


import os
import configparser


def get_config_by_name(section, name):
    file = os.path.join(os.path.dirname(os.path.abspath('.')), 'test.cfg')
    cf = configparser.ConfigParser()
    cf.read(file)
    return cf.get(section, name)
