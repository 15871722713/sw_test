# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-09-05 21:09:09
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-06 12:39:54

import os
import time
import unittest
import logger
import tcl_cmd
from BeautifulReport import BeautifulReport as bf
from stc import send_packets

from sw_common_win import *

timestr = str(time.strftime("%Y%m%d%H%M%S"))
folder = os.path.dirname(os.path.abspath(__file__))
filename = 'test_daisy_chain_test_{}'.format(timestr)
logname = '{}/log/log_daisy_chain_test_{}.log'.format(folder, timestr)

num = 8


def config_sw(cli, num):
    cli.send_cmd(cli.p_sw_privilege, 'vlan batch 100')
    cli.send_cmd(cli.p_sw_privilege, 'vlan 100')
    cli.send_cmd(None, 'port GigabitEthernet  0/0/1 to 0/0/{}'.format(num))
    cli.send_cmd(None, 'quit')


def delete_sw_cfg(cli, num):
    cli.send_cmd(cli.p_sw_privilege, 'vlan 100')
    cli.send_cmd(None, 'undo port GigabitEthernet  0/0/1 to 0/0/{}'.format(num))
    cli.send_cmd(None, 'quit')
    cli.send_cmd(cli.p_sw_privilege, 'undo vlan batch 100')
    if cli.sw.read_until(b'[\s\S]*Continue?[Y/N]:', timeout=5):
        cli.send_cmd(None, 'y')


class TestDaisyChain(unittest.TestCase):
    """docstring for TestDaisyChain"""
    @classmethod
    def setUpClass(self):
        logger.set_log_level(logger.DEBUG)
        logger.logfile(logname)
        logger.log('Set up test')
        global cli, stc
        cli = sw_consele()
        cli.login(sw_ip)
        config_sw(cli, num)
        stc = send_packets()

    def test001MaxMacTest(self):
        logger.log('Start to test')
        stc.main(tcl_cmd.cmds)
        stc.get_status()

    @classmethod
    def tearDownClass(self):
        logger.log('Tearing down test')
        delete_sw_cfg(cli, num)
        logger.close_log_file()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDaisyChain))
    run = bf(suite)
    run.report(filename=filename, report_dir='result', description='test_daisy_chain_test')
