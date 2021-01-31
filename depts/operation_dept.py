#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author : microfat
# @time   : 01/26/21 20:40:44
# @File   : operation_dept.py

import time
import logging

# logger config
logger = logging.getLogger("operation        ")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter("\x1b[93;21m[%(asctime)s] %(name)s:%(levelname)s: %(message)s\x1b[0m")
ch.setFormatter(formatter)

logger.addHandler(ch)

# ops job description
def ops(production_line, total_workshop):
    logger.info("Operation Dept start...")
    while True:
        mq_log = "monitor line size:"
        for i in range(total_workshop):
            mq_log += "line"+str(i)+"-> ("+str(production_line[i].qsize())+"),  "
        logger.info(mq_log)
        time.sleep(1)