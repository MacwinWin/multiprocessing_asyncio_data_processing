#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author : microfat
# @time   : 01/26/21 20:40:10
# @File   : purchasing_dept.py

import struct
import socket
import random
import logging
import time

# logger config
logger = logging.getLogger("Purchasing       ")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter("\x1b[94;21m[%(asctime)s] %(name)s:%(levelname)s: %(message)s\x1b[0m")
ch.setFormatter(formatter)

logger.addHandler(ch)

# generate random ip
def _generate_ip():
    source = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    destination = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    return source, destination

# buyer job description(put material to production line every some time)
def buyer(production_line, test_data, total_workshop):
    logger.info("Purchasing Dept start...")
    start = time.time()
    count = 0
    try:
        while True:
            count += 1
            if time.time() - start > 1:
                start = time.time()
                logger.info("Purchased {} in 1 second".format(count))
                count = 0

            material = test_data[0]
            # generate random souorce and destination ip
            source, destination = _generate_ip()
            material["src"] = source
            material["dst"] = destination
            # XOR(hash(source), hash(destination)) as material key
            material["pid"] = hash(source) ^ hash(destination)
            # use remainder as line num
            line_num = material["pid"] % total_workshop
            production_line[line_num].put([material])

            time.sleep(0.0000001)
    except Exception as e:
        logger.error(e)