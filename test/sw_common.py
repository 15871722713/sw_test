# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-21 15:16:17
# @Last Modified by:   JinHua
# @Last Modified time: 2019-08-23 10:50:54

import re
import pexpect
import threading
import logger
from time import sleep
from random import randint
from scapy.all import *


# import platform
# system = platform.system()

sw_ip = '10.30.1.250'
sw_username = 'admin'
sw_password = 'admin123'
iface = 'eth2'  # sever interface which is connect to sw
max_mac_num = 10000  # It is best to be a multiple of 100


class my_thread(threading.Thread):
    """docstring for my_thread"""

    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)


class ubuntu_ssh(object):
    """docstring for ubuntu_ssh"""

    def __init__(self):
        self.ssh = pexpect.spawn('telnet {}'.format(sw_ip))
        self.user_promt_regex = '[\s\S]*>'
        self.privilege_prompt_regex = '[\s\S]*]'
        self.more = '[\s\S]*---- More ----'
        self.p_sw_user = 0
        self.p_sw_privilege = 1
        self.sw_prompts = [self.user_promt_regex, self.privilege_prompt_regex]
        self.mode_lists = ['user', 'privilege']
        self.username = sw_username
        self.password = sw_password
        self.ssh.logfile = open('sw_test.log', 'w')

    def login(self):
        logger.log('Start to login switch')
        i = self.ssh.expect('Username:', timeout=30)
        if i == 0:
            self.ssh.sendline(sw_username)
            i = self.ssh.expect('Password:', timeout=30)
            if i == 0:
                self.ssh.sendline(sw_password)
                if self.ssh.expect(self.user_promt_regex, timeout=5):
                    logger.log('Login sucessful')
        else:
            logger.log('Login Failed')

    def prompt_sw_user_to_privilege(self):
        logger.log('Change mode from user to privilege')
        self.ssh.sendline()
        self.ssh.expect(self.user_promt_regex, timeout=5)
        self.ssh.sendline('system-view')
        self.ssh.expect(self.privilege_prompt_regex, timeout=5)

    def prompt_sw_privilege_to_user(self):
        logger.log('Change mode from privilege to user')
        self.ssh.sendline()
        self.ssh.expect(self.privilege_prompt_regex, timeout=5)
        self.ssh.sendline('quit')
        self.ssh.expect(self.user_promt_regex, timeout=5)

    def get_sw_prompt(self, p, timeout=5):
        self.ssh.sendline()
        i = self.ssh.expect(self.sw_prompts, timeout=timeout)
        if i == self.p_sw_user:
            if p == self.p_sw_privilege:
                self.prompt_sw_user_to_privilege()
        elif i == self.p_sw_privilege:
            if p == self.p_sw_user:
                self.prompt_sw_privilege_to_user()

    def send_cmd(self, p, c):
        self.get_sw_prompt(p)
        self.ssh.sendline('')
        self.ssh.expect(self.sw_prompts[p], timeout=60)
        self.ssh.sendline(c)
        output = ''
        while True:
            a = self.ssh.expect([self.more, self.sw_prompts[p]], timeout=10)
            output += self.ssh.after
            if a == 0:
                self.ssh.sendline(' ')
            elif a == 1:
                self.ssh.sendline('')
                # print(self.ssh.before)
                self.ssh.expect(self.sw_prompts[p], timeout=10)
                break
        self.ssh.sendline('')
        self.ssh.expect(self.sw_prompts[p], timeout=10)
        logger.log('Send {} command:{}\routput is:{}'.format(self.mode_lists[p], c, output))
        return output


def arp_ping(srcmac, iface):
    logger.log('Send packet to iface:{},srcmac is:{}'.format(iface, srcmac))
    sendp(Ether(src=srcmac, dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.2"), count=1, verbose=False, iface=iface)


def generate_mac():
    logger.log('generate mac')
    return ":".join(["%02x" % x for x in map(lambda x: randint(0, 255), range(6))])


def send_packet(iface, max_mac_num):
    for x in range(0, max_mac_num):
        srcmac = generate_mac()
        arp_ping(srcmac, iface)


def send_packet_with_thread(max_mac_num):
    logger.log('Start to send packet.')
    threads = []
    a = 100
    num = max_mac_num / a
    for i in range(num):
        t = my_thread(send_packet, args=(iface, a))
        threads.append(t)
    for i in range(num):
        threads[i].start()
    for i in range(num):
        threads[i].join()
    logger.log('End send packet.')


def main():
    cli = ubuntu_ssh()
    cli.login()

    send_packet_with_thread(max_mac_num)
    output = cli.send_cmd(cli.p_sw_privilege, 'dis mac-add')
    m = re.findall('Total items displayed = (\d{1,6})', output)
    logger.log('Max mac is {}'.format(m[0]))


if __name__ == '__main__':
    main()
