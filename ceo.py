#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author : microfat
# @time   : 01/26/21 20:18:18
# @File   : factory.py

import logging

from multiprocessing import Process, cpu_count, Queue
import aioprocessing

from depts import purchasing_dept, production_dept, transportation_dept, supervision_dept
from design import product_design
from raw_material import data

# logger config
logger = logging.getLogger("Factory          ")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter("\x1b[30;47m[%(asctime)s] %(name)s:%(levelname)s: %(message)s\x1b[0m")
ch.setFormatter(formatter)

logger.addHandler(ch)

# total production line according to cpu core
total_workshop = cpu_count() - 3

if __name__ == "__main__":
    # every workshop has one production line(thread-safe synchronize message queue)
    production_line = [Queue() for i in range(total_workshop)]
    # all production lines share one transportation line(thread-safe asynchronous message queue)
    transportation_line = aioprocessing.AioJoinableQueue()

    # one purchasing dept(single process)
    purchasing = Process(target=purchasing_dept.buyer, args=(production_line, data.test_data, total_workshop))
    # one supervision dept(single process)
    supervision = Process(target=supervision_dept.supervisor, args=(production_line, total_workshop))
    # multi workshop(multi production line) and different job position(multi processes + multi threads + multi coroutines)
    logger.info(f"Total {total_workshop} workshop")
    workshop_pool = []
    for line_num, line in enumerate(production_line):
        p = Process(target=production_dept.director, args=(line_num, line, transportation_line, product_design.blueprint))
        p.start()
        workshop_pool.append(p)
    # one transportation dept and two different job position(sigle process + multi coroutine)
    transportation = Process(target=transportation_dept.dispatcher, args=(transportation_line,))

    # start every dept
    purchasing.start()
    supervision.start()
    transportation.start()
    purchasing.join()
    supervision.join()
    for workshop in workshop_pool:
        workshop.join()
    transportation.join()