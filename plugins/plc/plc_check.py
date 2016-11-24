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





class PLCCheck(CheckBase):
    def __init__(self, plugin):

        # log.debug(__file__)



        super(PLCCheck, self).__init__(__file__, plugin)

        # self.conf = conf
        log.debug(self.conf)
        log.debug(">>>" * 20)




    def connect(self):
        """ connect ak host """

        self.plc.connect()

    def disconnect(self):

        self.plc.disconnect()

    def query(self,cmd):

        if 'RED' in cmd:
            data_6 = self.plc.readbytes_8_new(1, 6, 1)[0]  # read addr 6.0~6.7

            data_7 = self.plc.readbytes_8_new(1, 7, 1)[0]
            data_8 = self.plc.readbytes_long_new(1, 8, 2)[0]
            data_12 = self.plc.readbytes_long_new(1, 12, 2)[0]
            data_16 = self.plc.readbytes_long_new(1, 16, 2)[0]
            data_20 = self.plc.readbytes_long_new(1, 20, 2)[0]
            L =[((data_6 >> 4) & 0x01),
                ((data_6 >> 5) & 0x01),
                ((data_6 >> 6) & 0x01),
                ((data_6 >> 7) & 0x01),

                ((data_7) & 0x01),
                ((data_7 >> 1) & 0x01),
                ((data_7 >> 2) & 0x01),
                ((data_7 >> 3) & 0x01),

                data_8,
                data_12,
                data_16,
                data_20,
                ]
        return L


    def run(self):
        """ thread """

        while True:


            try:
                log.debug(self.g.queues.keys())
                log.debug(self.conf)

                self.plc = PLC(self.conf['host'].encode('utf8'), self.conf['port'])
                plc = self.plc


                plc.connect()
                cmd =self.get_cmd()

                log.debug(cmd)

                # cmd = 'ASTZ'
                rawdata = self.query(cmd['cmd'])
                data = self.inject_payload(int,rawdata)

                log.debug(data)

                self.put(data)

                plc.disconnect()
                         # time.sleep(3)
            except Exception as e:

                log.error(e)



