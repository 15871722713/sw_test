# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-09-04 12:50:49
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-05 21:05:36

import logger
import tcl_cmd
import tkinter


class stc(object):
    """docstring for stc"""

    def __init__(self):
        self.tclsh = tkinter.Tcl()

    def tcl_cmd(self, cmd):
        return self.tclsh.eval(cmd)


class send_packets(object):
    """docstring for send_packets"""

    def __init__(self):
        self.stc = stc()

    def main(self, cmds):
        logger.log("Start to send packets.")
        for cmd in cmds:
            self.stc.tcl_cmd(cmd)
        logger.log("Send packets finished.")

    def get_status(self):
        logger.log("Start to check result.")
        self.stc.tcl_cmd('set rxStreamResult [stc::get streamblock1 -children-rxstreamsummaryresults]')
        rxStreamResult = self.stc.tcl_cmd('stc::get $rxStreamResult -DroppedFrameCount')
        self.stc.tcl_cmd('set rxStreamResult [stc::get streamblock2 -children-rxstreamsummaryresults]')
        txStreamResult = self.stc.tcl_cmd('stc::get $rxStreamResult -DroppedFrameCount')
        logger.log('rx dropCount = {} , tx dropCount = {}'.format(rxStreamResult, txStreamResult))
        return rxStreamResult, txStreamResult


if __name__ == '__main__':
    a = send_packets()
    a.main(tcl_cmd.cmds)
    rxStreamResult, txStreamResult = a.get_status()
    print(rxStreamResult)
    print(type(rxStreamResult))
