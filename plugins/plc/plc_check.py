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

        if 'RED_B' in cmd:
            data_6 = self.plc.readbytes_8_new(11, 6, 1)[0]  # read addr 6.0~6.7

            data_7 = self.plc.readbytes_8_new(11, 7, 1)[0]
            data_8 = self.plc.readbytes_long_new(11, 8, 2)[0]
            data_12 = self.plc.readbytes_long_new(11, 12, 2)[0]
            data_16 = self.plc.readbytes_long_new(11, 16, 2)[0]
            data_20 = self.plc.readbytes_long_new(11, 20, 2)[0]
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

        elif 'RED_A' in cmd:
            data_0 = self.plc.readbytes_8_new(11, 0, 1)[0]
            data_1 = self.plc.readbytes_8_new(11, 0, 1)[0]
            data_2 = self.plc.readbytes_8_new(11, 0, 1)[0]
            
            data_8 = self.plc.readbytes_long_new(11, 8, 4)[0]
            data_12 = self.plc.readbytes_long_new(11, 12, 4)[0]
            data_16 = self.plc.readbytes_long_new(11, 16, 4)[0]
            data_20 = self.plc.readbytes_long_new(11, 20, 4)[0]
            data_24 = self.plc.readbytes_long_new(11, 24, 4)[0]
            data_28 = self.plc.readbytes_long_new(11, 28, 4)[0]
            data_32 = self.plc.readbytes_long_new(11, 32, 4)[0]
            data_36 = self.plc.readbytes_long_new(11, 36, 4)[0]
            
            '''
            data_8 = self.plc.readbytes(11, 7, 4)[1]
            data_12 = self.plc.readbytes(11, 11, 4)[1]
            data_16 = self.plc.readbytes(11, 15, 4)[1]
            data_20 = self.plc.readbytes(11, 19, 4)[1]
            data_24 = self.plc.readbytes(11, 23, 4)[1]
            data_28 = self.plc.readbytes(11, 27, 4)[1]
            data_32 = self.plc.readbytes(11, 31, 4)[1]
            data_36 = self.plc.readbytes(11, 35, 4)[1]
            '''
            
            data_56 = self.plc.readbytes_8_new(11, 56, 1)[0]
            data_57 = self.plc.readbytes_8_new(11, 57, 1)[0]
            data_58 = self.plc.readbytes_8_new(11, 58, 1)[0]
            data_59 = self.plc.readbytes_8_new(11, 59, 1)[0]
           

            L = [((data_0 ) & 0x01),
                 ((data_0 >> 1) & 0x01),
                 ((data_0 >> 2) & 0x01),
                 ((data_0 >> 3) & 0x01),
                 ((data_0 >> 4) & 0x01),
                 ((data_0 >> 5) & 0x01),
                 ((data_0 >> 6) & 0x01),
                 ((data_0 >> 7) & 0x01),

                 ((data_1 >> 4) & 0x01),
                 ((data_1 >> 5) & 0x01),
                 ((data_1 >> 7) & 0x01),

                 ((data_2 ) & 0x01),
                 ((data_2 >> 2) & 0x01),
                 ((data_2 >> 3) & 0x01),
                 ((data_2 >> 5) & 0x01),
                 ((data_2 >> 6) & 0x01),

                 data_8,
                 data_12,
                 data_16,
                 data_20,
                 data_24,
                 data_28,
                 data_32,
                 data_36,

                 ((data_56 ) & 0x01),
                 ((data_56 >> 1) & 0x01),
                 ((data_56 >> 2) & 0x01),
                 ((data_56 >> 3) & 0x01),
                 ((data_56 >> 4) & 0x01),
                 ((data_56 >> 5) & 0x01),
                 ((data_56 >> 6) & 0x01),
                 ((data_56 >> 7) & 0x01),

                 ((data_57) & 0x01),
                 ((data_57 >> 1) & 0x01),
                 ((data_57 >> 2) & 0x01),
                 ((data_57 >> 3) & 0x01),
                 ((data_57 >> 4) & 0x01),
                 ((data_57 >> 5) & 0x01),
                 ((data_57 >> 6) & 0x01),
                 ((data_57 >> 7) & 0x01),

                 ((data_58) & 0x01),
                 ((data_58 >> 1) & 0x01),
                 ((data_58 >> 2) & 0x01),
                 ((data_58 >> 3) & 0x01),
                 ((data_58 >> 4) & 0x01),
                 ((data_58 >> 5) & 0x01),
                 ((data_58 >> 6) & 0x01),
                 ((data_58 >> 7) & 0x01),

                 ((data_59) & 0x01),
                 ((data_59 >> 1) & 0x01),
                 ((data_59 >> 2) & 0x01),
                 ((data_59 >> 3) & 0x01),
                 ((data_59 >> 4) & 0x01),
                 ((data_59 >> 5) & 0x01),
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



