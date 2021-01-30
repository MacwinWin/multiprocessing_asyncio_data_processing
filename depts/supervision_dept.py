#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author : microfat
# @time   : 01/26/21 20:40:44
# @File   : supervision_dept.py

import time
import logging

# logger config
logger = logging.getLogger("Supervision      ")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter("\x1b[93;21m[%(asctime)s] %(name)s:%(levelname)s: %(message)s\x1b[0m")
ch.setFormatter(formatter)

logger.addHandler(ch)

# supervisor job description
def supervisor(production_line, total_workshop):
    logger.info("Supervision Dept start...")
    while True:
        mq_log = "supervise line size:"
        for i in range(total_workshop):
            mq_log += "line"+str(i)+"-> ("+str(production_line[i].qsize())+"),  "
        logger.info(mq_log)
        time.sleep(1)