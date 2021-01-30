#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author : microfat
# @time   : 01/26/21 20:40:34
# @File   : transportation_dept.py

import time
import datetime
import logging
import pandas as pd
import asyncio

# logger config
logger = logging.getLogger("Transportation   ")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter("\x1b[96;21m[%(asctime)s] %(name)s:%(levelname)s: %(message)s\x1b[0m")
ch.setFormatter(formatter)

logger.addHandler(ch)

# stevedore job description(one stevedore transport production from transportation line to warehouse timely)
async def stevedore(transportation_line, warehouse):
    while True:
        production = await transportation_line.coro_get()
        if production["pclass"] not in warehouse:
            warehouse[production["pclass"]] = pd.DataFrame()

        df=pd.DataFrame(production["product"])
        warehouse[production["pclass"]] = warehouse[production["pclass"]].append(df)

# driver job description(one driver transport production from warehouse to destination every some time)
async def driver(warehouse):
    while True:
        await asyncio.sleep(5)
        for production_class in list(warehouse.keys()):
            if not warehouse[production_class].empty:
                # ...
                del warehouse[production_class]

async def main(transportation_line):
    warehouse = {}
    # task list
    tasks = [
        asyncio.create_task(stevedore(transportation_line, warehouse)),
        asyncio.create_task(driver(warehouse))
    ]
    logger.info("Transportation Dept start...")
    await asyncio.wait(tasks)

# dispatcher job description(control the transportation)
def dispatcher(transportation_line):
    asyncio.run(main(transportation_line))