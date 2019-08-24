# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-23 16:46:34
# @Last Modified by:   JinHua
# @Last Modified time: 2019-08-24 20:09:18

import time
import unittest
import logger
from BeautifulReport import BeautifulReport as bf


from sw_common_win import *


class TestPortRate(unittest.TestCase):
    """docstring for TestPortRate"""
    @classmethod
    def setUpClass(self):
        logger.set_log_level(logger.DEBUG)
        logger.log('Set up test')
        global cli, old_auto_negotiation, old_speed
        cli = sw_consele()
        cli.login(sw_ip)
        old_auto_negotiation = get_output(cli, cli.p_sw_privilege,
                                          'dis interface GigabitEthernet 0/0/2', r'Negotiation: ([A-Z]{6,7})')
        old_speed = int(get_output(cli, cli.p_sw_privilege,
                                   'dis interface GigabitEthernet 0/0/1', r'Speed : ([01]{2,4})'))
        logger.log('Old port rate is {},port auto negotiation is {}'.format(old_speed, old_auto_negotiation))

    def test001PortRate1000MTest(self):
        logger.log('Start to test')
        auto_negotiation = get_output(cli, cli.p_sw_privilege,
                                      'dis interface GigabitEthernet 0/0/2', r'Negotiation: ([A-Z]{6,7})')
        cli.send_cmd(cli.p_sw_privilege, 'interface GigabitEthernet 0/0/2')
        if auto_negotiation == "ENABLE":
            cli.send_cmd('undo negotiation auto')
        cli.send_cmd(None, 'speed 1000')
        cli.send_cmd(None, 'quit')
        time.sleep(2)
        speed = get_output(cli, cli.p_sw_privilege, 'dis interface GigabitEthernet 0/0/1', r'Speed : ([01]{2,4})')
        self.assertEqual(int(speed), 1000, msg="Port rate is not same")

    def test002PortRate100MTest(self):
        logger.log('Start to test')
        auto_negotiation = get_output(cli, cli.p_sw_privilege,
                                      'dis interface GigabitEthernet 0/0/2', r'Negotiation: ([A-Z]{6,7})')
        cli.send_cmd(cli.p_sw_privilege, 'interface GigabitEthernet 0/0/2')
        if auto_negotiation == "ENABLE":
            cli.send_cmd('undo negotiation auto')
        cli.send_cmd(None, 'speed 100')
        cli.send_cmd(None, 'quit')
        time.sleep(2)
        speed = get_output(cli, cli.p_sw_privilege, 'dis interface GigabitEthernet 0/0/1', r'Speed : ([01]{2,4})')
        self.assertEqual(int(speed), 100, msg="Port rate is not same")

    def test003PortRate10MTest(self):
        logger.log('Start to test')
        auto_negotiation = get_output(cli, cli.p_sw_privilege,
                                      'dis interface GigabitEthernet 0/0/2', r'Negotiation: ([A-Z]{6,7})')
        cli.send_cmd(cli.p_sw_privilege, 'interface GigabitEthernet 0/0/2')
        if auto_negotiation == "ENABLE":
            cli.send_cmd('undo negotiation auto')
        cli.send_cmd(None, 'speed 10')
        cli.send_cmd(None, 'quit')
        time.sleep(2)
        speed = get_output(cli, cli.p_sw_privilege, 'dis interface GigabitEthernet 0/0/1', r'Speed : ([01]{2,4})')
        self.assertEqual(int(speed), 10, msg="Port rate is not same")

    @classmethod
    def tearDownClass(self):
        logger.log('Tearing down test')
        # cli.send_cmd(cli.p_sw_privilege, 'mac-address aging-time {}'.format(aging_time))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPortRate))
    run = bf(suite)
    filename = 'test_port_rate_test_' + str(time.strftime("%Y%m%d%H%M%S"))
    run.report(filename=filename, report_dir='result', description='test_port_rate_test')
