# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-22 14:24:44
# @Last Modified by:   JinHua
# @Last Modified time: 2019-08-30 16:41:41

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import time
import unittest
import logger
import HTMLTestRunner

from sw_common_win import *

timestr = str(time.strftime("%Y%m%d%H%M%S"))
filename = 'test_mac_capacity_test_{}.html'.format(timestr)
logname = 'log_mac_capacity_test_{}.log'.format(timestr)


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
        # send_packet_with_thread(max_mac_num)
        # send_packets(max_mac_num)
        max_mac = int(get_output(cli, cli.p_sw_privilege, 'dis mac-address total-number', r'\s\S.*?(\d{1,7})'))
        logger.log('Max mac is {}'.format(max_mac))

    @classmethod
    def tearDownClass(self):
        logger.log('Tearing down test')
        cli.send_cmd(cli.p_sw_privilege, 'mac-address aging-time {}'.format(aging_time))
        logger.close_log_file()


fp = open('result/{}'.format(filename), 'wb')
suite = unittest.TestLoader().loadTestsFromTestCase(TestMacCapacity)
runner = HTMLTestRunner.HTMLTestRunner(fp)
runner.run(suite)
fp.close()
