# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-22 14:24:44
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-06 13:23:46

import os
import time
import unittest
import logger


from sw_common_win import *

timestr = str(time.strftime("%Y%m%d%H%M%S"))
folder = os.path.dirname(os.path.abspath(__file__))
filename = 'test_mac_capacity_test_{}'.format(timestr)
logname = '{}/log/log_mac_capacity_test_{}.log'.format(folder, timestr)


class TestMacCapacity(unittest.TestCase):
    """docstring for TestMacCapacity"""
    @classmethod
    def setUpClass(self):
        logger.set_log_level(logger.DEBUG)
        logger.logfile(logname)
        logger.log('Set up test')
        global cli, aging_time
        cli = sw_consele()
        cli.login(sw_ip)
        aging_time = int(get_output(cli, cli.p_sw_privilege, 'dis mac-address aging-time', r'\s\S.*?(\d{1,7})\s\S.*?'))
        cli.send_cmd(cli.p_sw_privilege, 'mac-address aging-time 0')

    def test001MaxMacTest(self):
        logger.log('Start to test')
        max_mac = int(get_output(cli, cli.p_sw_privilege, 'dis mac-address total-number', r'\s\S.*?(\d{1,7})'))
        logger.log('Max mac is {}'.format(max_mac))

    @classmethod
    def tearDownClass(self):
        logger.log('Tearing down test')
        cli.send_cmd(cli.p_sw_privilege, 'mac-address aging-time {}'.format(aging_time))

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMacCapacity))
    run = testReport(suite)
    run.report(filename=filename, report_dir='result', description='test_mac_capacity_test')
    logger.close_log_file()

