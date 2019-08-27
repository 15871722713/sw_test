# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-24 20:44:58
# @Last Modified by:   JinHua
# @Last Modified time: 2019-08-27 16:44:20


import os
import ConfigParser


def get_config_by_name(section, name):
    file = os.path.join(os.path.dirname(os.path.abspath('.')), 'test.cfg')
    cf = ConfigParser.ConfigParser()
    cf.read(file)
    return cf.get(section, name)
