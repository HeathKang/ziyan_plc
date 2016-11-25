# -*- coding: utf-8 -*-

"""
dam_data handler

"""

from __future__ import absolute_import

import msgpack
import time
from Queue import Queue  # just for test

from logbook import Logger

log = Logger('plc_handler')

from maboio.lib.redis_lib import RedisClient

from ziyan.lib.handler_base import HandlerBase


class PLCHandler(HandlerBase):
    """ msg processor for Dam"""

    def __init__(self, plugin):
        """
        channel

        """

        super(PLCHandler, self).__init__(__file__, plugin)

        log.debug('---' * 25)

        log.debug('---' * 25)

        self.red = RedisClient(self.conf['redis'])
        self.red.load_script(self.conf['output']['enqueue_script'])

    def process(self, **kwargs):
        """
        process

        """
        rtn = self.red.enqueue(eqpt_no=kwargs['eqpt_no'],
                               timestamp=kwargs['timestamp'],
                               cmd=kwargs['cmd'],
                               rawdata=msgpack.packb(kwargs['rawdata']),
                               data=msgpack.packb(kwargs['data']),
                               measurement=kwargs['measurement'])
        log.debug(rtn)

    def run(self):
        """
        loop

        """
        while True:


            ### get  msg from msg_queue
            '''
            timestamp = time.time()
            data_test = [20, 20, 20, 20]
            fields = {'uuid': 1,
                      'timestamp': timestamp,
                      'type': 1,
                      'channel': self.channel,
                      'interval': 10,
                      'payload': data_test
                      }
            '''

            fields = self.get()

            log.debug(fields)

            eqpt_no = self.conf['plc_equipment']['equipmentno']

            timestamp = fields['timestamp']

            # log.debug(button_status)

            measurement = self.conf['plc_measurement']['measurement']
            data = fields['payload']
            rawdata = fields['payload']
            log.debug(data)
            # msg = {'uuid':uid, 'timestamp':timestamp,'type':type, 'channel':self.channel, 'interval':interval, 'payload ':payload}
            self.process(eqpt_no=eqpt_no,
                         timestamp=int(timestamp * (1000)),
                         cmd='RED',
                         rawdata=rawdata,
                         data=data,
                         measurement=measurement)
            # msg_queue.task_done()
            print("*" * 50)
            log.debug(int(timestamp))
            print("*" * 50)



















