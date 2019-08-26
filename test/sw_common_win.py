# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-21 15:16:17
# @Last Modified by:   JinHua
# @Last Modified time: 2019-08-25 20:16:23


import re
import telnetlib
import threading
import logger
from time import sleep
from random import randint
from config_read import get_config_by_name
from scapy.all import *


# import platform
# system = platform.system()

sw_ip = get_config_by_name('sw', 'ip')
sw_username = get_config_by_name('sw', 'username')
sw_password = get_config_by_name('sw', 'password')
iface = get_config_by_name('mac', 'iface')
max_mac_num = int(get_config_by_name('mac', 'max_mac'))


class my_thread(threading.Thread):
    def __init__(self, name, num):
        threading.Thread.__init__(self)
        self.name = name
        self.num = num

    def run(self):
        logger.log('Start thread {}'.format(self.name))
        send_packet(self.num)


class sw_consele(object):
    """docstring for ubuntu_ssh"""

    def __init__(self):
        self.sw = telnetlib.Telnet()
        self.user_promt_regex = b'[\s\S]*>'
        self.privilege_prompt_regex = b'[\s\S]*]'
        self.more = b'[\s\S]*---- More ----'
        self.p_sw_user = 0
        self.p_sw_privilege = 1
        self.sw_prompts = [self.user_promt_regex, self.privilege_prompt_regex]
        self.mode_lists = ['user', 'privilege']
        self.username = sw_username
        self.password = sw_password
        # self.ssh.logfile = open('sw_test.log', 'w')

    def login(self, sw_ip):
        logger.log('Start to login switch')
        try:
            self.sw.open(sw_ip)
        except Exception as e:
            logger.log('{} network is unreachable'.format(sw_ip))
            return False
        if self.sw.read_until(b'Username:', timeout=30):
            self.sw.write(self.username.encode('ascii') + b'\n')
            if self.sw.read_until(b'Password:', timeout=30):
                self.sw.write(self.password.encode('ascii') + b'\n')
                sleep(1)
                if self.sw.read_until(b'<HUAWEI>', timeout=30):
                    logger.log('Login sucessful')
        else:
            logger.log('Login Failed')

    def prompt_sw_user_to_privilege(self):
        logger.log('Change mode from user to privilege')
        self.sw.write(b'\n')
        self.sw.read_until(self.user_promt_regex, timeout=5)
        self.sw.write(b'system-view\n')
        self.sw.read_until(self.privilege_prompt_regex, timeout=5)

    def prompt_sw_privilege_to_user(self):
        logger.log('Change mode from privilege to user')
        self.sw.write(b'\n')
        self.sw.read_until(self.privilege_prompt_regex, timeout=5)
        self.sw.write(b'quit\n')
        self.sw.read_until(self.user_promt_regex, timeout=5)

    def get_sw_prompt(self, p, timeout=5):
        self.sw.write(b'\n')
        i, m, text = self.sw.expect(self.sw_prompts, timeout=timeout)
        if i == self.p_sw_user:
            if p == self.p_sw_privilege:
                self.prompt_sw_user_to_privilege()
        elif i == self.p_sw_privilege:
            if p == self.p_sw_user:
                self.prompt_sw_privilege_to_user()

    def send_cmd(self, p=None, c=None):
        if p:
            self.get_sw_prompt(p)
            self.sw.write(b'\n')
            self.sw.read_until(self.sw_prompts[p], timeout=10)
            self.sw.read_very_eager().decode('ascii')
            self.sw.write(c.encode('ascii') + b'\n')
            output = ''
            while True:
                a, m, text = self.sw.expect([self.more, self.sw_prompts[p]], timeout=10)
                # print(text)
                output += text.decode('ascii').replace(
                    '[42D                                          [42D', '\r').replace('---- More ----', '')
                if a == 0:
                    self.sw.write(b' \n')
                elif a == 1:
                    break
            # print(output)
            logger.log('Send {} command:{}\routput is:{}'.format(self.mode_lists[p], c, output))
            return output
        else:
            logger.log('Send config command : {}'.format(c))
            self.sw.write(c.encode('ascii') + b'\n')


def get_output(cli, p, c, r):
    output = cli.send_cmd(p, c)
    result = re.findall(r, output)
    if len(result) > 0:
        return result[0]
    else:
        logger.log('get_output error with command:{}'.format(c))
        raise 'error'


def arp_ping(srcmac, iface):
    logger.log('Send packet to iface:{},srcmac is:{}'.format(iface, srcmac))
    sendp(Ether(src=srcmac, dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.2"), count=1, verbose=False, iface=iface)


def generate_mac():
    return ":".join(["%02x" % x for x in map(lambda x: randint(0, 255), range(6))])


def send_packets(max_mac_num):
    flag = True
    mac_list = []
    while flag:
        mac = generate_mac()
        if mac not in mac_list:
            mac_list.append(mac)
        if len(mac_list) == max_mac_num:
            flag = False
    logger.log('mac list is :\r{}'.format(mac_list))
    for mac in mac_list:
        arp_ping(mac, iface)


def send_packet(max_mac_num):
    for x in range(0, max_mac_num):
        srcmac = generate_mac()
        arp_ping(srcmac, iface)


def send_packet_with_thread(max_mac_num):
    logger.log('Start to send packet.')
    threads = []
    a = 100
    num = int(max_mac_num / a)
    for i in range(num):
        t = my_thread('Tread{}'.format(i), a)
        threads.append(t)
    for i in range(num):
        threads[i].start()
    for i in range(num):
        threads[i].join()
    logger.log('End send packet.')


def main():
    send_packet_with_thread(10000)
    cli = sw_consele()
    cli.login()
    cli.send_cmd(cli.p_sw_privilege, 'interface GigabitEthernet 0/0/2')


if __name__ == '__main__':
    # main()
    send_packets(max_mac_num)
