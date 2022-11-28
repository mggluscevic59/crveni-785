#!/usr/bin/env python
import logging
import asyncio
import time
import datetime


from crystapp_04 import wrapper, temp_read, \
    GentleFileWriter, BROJ_MJERENJA, VREMENSKI_ODMAK

OPC_TEST = "178.238.237.121"
OPC_REAL = "192.168.0.118"


def blend_in(writer, temp):
    with writer as file:
        with open(writer.buffer_path, "r", encoding="UTF-8") as buffer:
            spectra = buffer.readlines()[1].split(",")
            spectra[1] = temp
            file.write(",".join([str(x) for x in spectra]))


def calc_wait(start:datetime, stop:datetime, delay):
    passed = int((stop - start).microseconds*0.001)
    logging.debug(passed)
    if passed > delay:
        return 0
    supstracted = delay - passed
    logging.debug(supstracted)
    return supstracted*0.001


async def main(log_level):
    writer = GentleFileWriter(".data/", ".buffer.csv")

    for _ in range(BROJ_MJERENJA):
        start_time = datetime.datetime.now()
        task1 = asyncio.create_task(temp_read(log_level, OPC_TEST))
        await wrapper(log_level, writer.buffer_path)
        blend_in(writer, await task1)
        end_time = datetime.datetime.now()

        await asyncio.sleep(calc_wait(start_time, end_time, VREMENSKI_ODMAK))


if __name__ == "__main__":
    FORMAT = '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # log level
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    # logging.basicConfig(level=logging.INFO, format=FORMAT)
    logging.getLogger("asyncua.client").setLevel(logging.WARNING)
    # logging.getLogger("wasatch").setLevel(logging.WARNING)
    # logging.getLogger("wasatch").setLevel(logging.INFO)
    # main(logging.DEBUG)
    asyncio.run(main(logging.DEBUG))
