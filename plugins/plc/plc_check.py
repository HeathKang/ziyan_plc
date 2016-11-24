# -*- coding: utf-8 -*-

"""
plugin for Modbus Client

"""
from __future__ import absolute_import

import os
import sys

import time

from logbook import Logger

log = Logger('plc_chk')

from maboio.lib.utils import fn_timer

# from lib.sharedq import SharedQ
from ziyan.lib.exceptions import NoDataException


from ziyan.lib.check_base import CheckBase
from ziyan.lib.plc_lib import PLC





class DAMCheck(CheckBase):
    def __init__(self, plugin):

        # log.debug(__file__)
        #


        super(DAMCheck, self).__init__(__file__, plugin)

        # self.conf = conf
        log.debug(self.conf)
        log.debug(">>>" * 20)
        self.plc = PLC(self.conf['host'],self.conf['port'])

        self.connect()

    def connect(self):
        """ connect ak host """

        self.mod.connect()

    def run(self):
        """ thread """

        while True:

            try:

                log.debug(self.g.queues.keys())

                cmd = self.get_cmd()
                plc = self.plc
                plc.connect()
                plc.readbytes(11, 4, 2)  # (start_add,offset)
                plc.writebytes(11, 4, 124)  # (db,start_add,offset)

                log.debug(cmd)

                # cmd = 'ASTZ'
                rawdata = plc.query(cmd['cmd'])
                data = self.inject_payload(int,rawdata)

                log.debug(data)

                self.put(data)



                                # time.sleep(3)
            except Exception as ex:

                log.error(ex)

                def main():
                    """ for test """
                    host = "192.168.1.10"
                    # host = "127.0.0.1"
                    plc = PLC(host, 102)
                    plc.connect()
                    plc.readbytes(11, 4, 2)  # (start_add,offset)
                    plc.writebytes(11, 4, 124)  # (db,start_add,offset)
                    '''


                    '''

                    # plc.readbytes(11,0,6)

                    plc.disconnect()