#!/usr/bin/env python
import logging
import asyncio
# import time
import datetime
import platform
import os
import psutil
import sys


from crystapp_04 import wrapper, temp_read, \
    GentleFileWriter, BROJ_MJERENJA, VREMENSKI_ODMAK


OPC_TEST = "178.238.237.121"
OPC_REAL = "192.168.0.118"


def blend_in(writer: GentleFileWriter, temp):
    with writer as file:
        with open(writer.buffer_path, "r", encoding="UTF-8") as buffer:
            spectra = buffer.readlines()[1].split(",")
            spectra[0] = datetime.datetime.now().strftime("%H:%M:%S")
            spectra[1] = temp
            # logging.info("%7.2f°C julabo t-1000", float(temp))
            logging.info("{0:7.2f}°C julabo t-1000".format(float(temp)))
            file.write(",".join([str(x) for x in spectra]))
            # if platform.system().lower()!="windows":
            #     file.write("\n")


def calc_wait(start:datetime.datetime, stop:datetime.datetime, delay):
    passed = int((stop - start).microseconds*0.001)
    # logging.debug("%4d miliseconds", passed)
    logging.debug("{0:5d} miliseconds".format(passed))
    if passed > delay:
        return 0
    supstracted = delay - passed
    # logging.info("%s miliseconds async sleep", supstracted)
    logging.info(f"{supstracted} miliseconds async sleep")
    return supstracted*0.001


async def main(log_level):
    writer = GentleFileWriter(".data/", ".buffer.csv")

    for i in range(BROJ_MJERENJA):
        start_time = datetime.datetime.now()
        logging.debug("started measurement")
        task1 = asyncio.create_task(temp_read(log_level, OPC_REAL))
        # task1 = asyncio.create_task(temp_read(log_level, OPC_TEST))
        await wrapper(log_level, writer.buffer_path)
        blend_in(writer, await task1)
        end_time = datetime.datetime.now()
        logging.debug("ended measurement")

        logging.debug([i, BROJ_MJERENJA])
        if i != (BROJ_MJERENJA - 1):
            await asyncio.sleep(calc_wait(start_time, end_time, VREMENSKI_ODMAK))


if __name__ == "__main__":
    os_used = sys.platform
    process = psutil.Process(os.getpid())  # Set highest priority for the python script for the CPU
    if os_used == "win32":  # Windows (either 32-bit or 64-bit)
        process.nice(psutil.REALTIME_PRIORITY_CLASS)
    elif os_used == "linux":  # linux
        # process.nice(psutil.IOPRIO_HIGH)
        pass
    else:  # MAC OS X or other
        process.nice(20) 
    FORMAT = '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # log level
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    # logging.basicConfig(level=logging.INFO, format=FORMAT)
    logging.getLogger("asyncua.client").setLevel(logging.WARNING)
    # LOG_NAME = "wasatch.FeatureIdentificationDevice"
    # logging.getLogger(LOG_NAME).setLevel(logging.CRITICAL + 1)
    asyncio.run(main(logging.INFO))
