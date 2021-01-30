#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author : microfat
# @time   : 01/26/21 20:39:52
# @File   : production_dept.py

import time
import logging
import asyncio
from threading import Thread

# logger config
def config_logger(line_num):
    logger = logging.getLogger("Production_Line")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    formatter = logging.Formatter("\x1b[32;21m[%(asctime)s] %(name)s_{}:%(levelname)s: %(message)s\x1b[0m".format(line_num))

    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger

# every worker's contract period
contract_period = 5

# director job description
def director(line_num, line, transportation_line, blueprint):
    logger = config_logger(line_num)
    logger.info(f"Production Line:{line_num} start...")
    vice_director = asyncio.new_event_loop()
    asyncio.set_event_loop(vice_director)
    resource = Thread(target = lambda x: x.run_forever(), args=(vice_director,))
    resource.daemon = True
    resource.start()
    worker_roster = {}
    # assign one monitor to monitor the worker_roster size
    asyncio.run_coroutine_threadsafe(monitor(line_num, worker_roster, logger), vice_director)

    while True:
        material_list = line.get()
        for material in material_list:
            pid = material["pid"]
            # if the project haven't worker to response yet, create a new worker
            if pid not in worker_roster:
                worker_roster[pid] = {}
                worker_roster[pid]['line'] = asyncio.Queue(loop=vice_director)
                work_task = asyncio.run_coroutine_threadsafe(worker(pid, worker_roster, transportation_line, blueprint), vice_director)
                check_task = asyncio.run_coroutine_threadsafe(inspector(pid, transportation_line, worker_roster), vice_director)
                worker_roster[pid]['work_task'] = work_task
                worker_roster[pid]['check_task'] = check_task
                # siging the contract
                timeout_task = asyncio.run_coroutine_threadsafe(contract(pid, worker_roster), vice_director)
                worker_roster[pid]['timeout_task'] = timeout_task
            # if the project already have worker to response, renew the contract
            else:
                # cancel the old contract
                worker_roster[pid]['timeout_task'].cancel()
                # siging the new contract
                timeout_task = asyncio.run_coroutine_threadsafe(contract(pid, worker_roster), vice_director)
                worker_roster[pid]['timeout_task'] = timeout_task
            # put the raw material to some worker's mq
            asyncio.run_coroutine_threadsafe(
                worker_roster[pid]['line'].put(material), vice_director)

# worker's job description
async def worker(pid, worker_roster, transportation_line, blueprint):
    while True:
        # First: get raw materials from mq
        material = await worker_roster[pid]["line"].get()
        # your business program there ...
        # Secondly: create product
        pclass, product=blueprint(material)
        # Finally: put product to mq
        await transportation_line.coro_put({"pclass":pclass, "product":product})

# inspector's job description
async def inspector(pid, transportation_line, worker_roster):
    while True:
        # your own program there ...
        await asyncio.sleep(2)

# every worker's contract, if worker didn't get any raw materials until the expiration of contract, the worker will leave
async def contract(pid, worker_roster):
    await asyncio.sleep(contract_period)
    worker_roster[pid]['work_task'].cancel()
    worker_roster[pid]['check_task'].cancel()
    worker_roster.pop(pid)

# monitor the worker_roster size(coroutine)
async def monitor(line_num, worker_roster, logger):
    while True:
        worker_roster_log = "monitor worker roster size:-> ("+str(len(worker_roster))+")"
        logger.info(worker_roster_log)
        await asyncio.sleep(1)