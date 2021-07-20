<p align="center">
    <img src="./first_image.jpg">

[elenabsl/Shutterstock](https://www.shutterstock.com/image-vector/innovative-contemporary-smart-industry-product-design-1160095369)

------
# multiprocessing_asyncio_data_processing

[![Documentation](https://img.shields.io/badge/Python-3.7%2B-green.svg)](https://docs.python.org/3/library/asyncio-task.html#asyncio.run)

A program template for processing data concurrently, modules have used including Python3 built-in modules like multiprocessing, threading, asyncio, etc., a third-party modules [aioprocessing](https://github.com/dano/aioprocessing).

## Table of Contents
* [Overview](#Overview)
* [Detail](#Detail)
* [How To Use](#How-To-Use)
* [Test](#Test)
* [To-Do List](#To-Do-List)
* [Caption](#Caption)
## Overview
This program will put the test data generated by a process to multiple message queues which will be received by multiple processes. These procsses will get data from their own message queue, process these data, and then put processed-data to a shared message queue(aioprocessing [1](#1)), another single process will get data from the shared message queue and do some thing like exportation.

*The overview diagram of this project:*

<p align="center">
    <img src="./overview.svg">

## Detail

In order to make my explaination easier to understand, I abstract the architecture to the factory in our real world. The whole data processing process can be seen as the production process. I rename the object name to the real world name. Now I will start my explaination like company introduction in a roadshow.

*The organization structure*

<p align="center">
    <img src="./structure.svg">

Description of this departments and jobs:
- [CEO](./ceo.py): 
    1. Deploy workshop number according to the resource(CPU cores).
    2. Create prouction line to every workshop(thread-safe synchronize message queue), create a transportation line(thread-safe asynchronous message queue).
    3. Start workshops, purchasing dept, operation dept, transportation dept.
- [Purchasing Department](./depts/purchasing_dept.py):
    - Buyer:
        1. Purchasing raw material and paste product id(pid) tag. Some different raw materials may belong to one product(have the same pid). 
        2. Put the raw material to the prouction line it belongs to.
- [Production Department](./depts/production_dept.py):
    - workshop_0:
        - Director: Every workshop has a director
            1. Manage Vice Director, Monitor.
            2. Get material from production line, assign it to some worker according to its 'pid' in worker roster.
            3. Sign the contract [2](#2) with new worker, renew the contract with old worker if a new material belonging to he arrived.
            - Vice Director:
                1. Occupy a half of the workshop resource(GIL) to manage workers and inspectors.
                2. Only allocate resource to workers with material.
                - Worker: 
                    1. Every worker has a conveyor belt, they get material from the exclusive conveyor belt.
                    2. According to the product blueprint to assembly the product.
                    3. Paste the product class(pclass) tag and put it to transportation line.
                    4. Every worker have a contract, every time get new material, director will renew the contract. If the worker don't get the  new material before the contract expires, the worker will be fired.
                - Inspector:
                    1. One inspector inspect one worker every other time and do something.
            - Monitor:
                1. Reoirt directly to the Director and be accountable to the Director.
                2. Check the worker roster every other time
    - workshop_1:
    - ...
    - workshop_n:
- [Transportation dept](./depts/transportation_dept.py):
    - Dispatcher:
        1. Manage stevedore and driver.
        2. Manage warehouse.
        - Stevedore:
            1. Get product from transportation line.
            2. Do something, such as pakaging(pandas).
            3. Put it to warehouse according to product class(pclass)
        - Driver:
            1. Get all products from warehouse every other time.
- [Operation dept](./depts/operation_dept.py):
    - Ops:
        1. Monitor all production lines every other time

## How To Use
```bash
# build image
>>> docker build -t test:1.0 .
# run the image as a container
>>> docker run -i -t -d -v $(pwd):/app --name test test:1.0
>>> docker exec -i -t test /bin/bash
>>> python3 ceo.py
```

This project only provide the 'factory', as for what 'product' to make you need create your own '[blueprint](./design/product_design)'.
## Test
I test this project on my MacBook Pro 16-inch, i7 2.6GHz.
Deploied resource to the Docker of CPUs 8, 8G RAM.
As we can see the project purchase 5000+ materials every 1 second, and give them to 5 workshop to make product. Every production line has no backlog. Every workshop's worker roster size stable at around 5000.
<p align="center">
    <img src="./limit_20s.gif">
But if there is no limit of purching speed, it will lead to the quantity of raw materials far exceeds the actual production capacity. A large backlog of raw materials on the production line. Seriously reduce the performance of the production line. The workshop was unable to obtain sufficient raw materials, resulting in a significant drop in the company's production capacity.
<p align="center">
    <img src="./nolimit_20s.gif">
So the best solution is to determine the number of workshops based on the number of resources(number of CPU cores), and then reasonably set the procurement speed, so that the raw material procurement speed matches the actual production capacity, and there is no backlog in the production line.
## To-Do List
- [ ] Continuously optimize the code to improve the running speed
- [ ] Add type hints
## Caption
### 1: 
Aioprocessing in this project is only used its AioJoinableQueue which is a thread-safe asynchronous queue to gather the output from multi processes. But because of being made of pure Python, the speed of AioJoinableQueue is not satisfactory. So it can be replaced in the future.
### 2:
Contract mechanism is in order to immediately determine the cancelling of the order after a period of time and fire the worker. Save the resources.