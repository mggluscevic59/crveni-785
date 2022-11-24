#!/usr/bin/env python
import logging
import asyncio
import time
import datetime
import sys


from demo_custom import WasatchDemo
from crystapp_04 import temp_read, GentleFileWriter


INTEGRACIJSKO_VRIJEME = 500 # milisecond
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 3
VREMENSKI_ODMAK = 60000 # milisecond


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
    return supstracted


def main():
    # NOTE: julabo i.p. address - 192.168.0.101
    buffer_path, data_path, opc_ip = ".buffer.csv", ".data/", "192.168.0.118"
    # logging.info(asyncio.run(temp_read(logger, opc_ip)))
    # temp = "100.00"
    writer = GentleFileWriter(data_path, buffer_path)
    # Raman instance
    mock_argv = [
        "--outfile="+str(buffer_path),
        "--max=1",
        "--delay-ms=0",
        "--integration-time-ms="+str(INTEGRACIJSKO_VRIJEME),
        "--ascii-art",
        "--scans-to-average="+str(BROJ_OCITANJA_ZA_INTERPOLACIJU),
        "--log-leve="+logging.getLevelName(logging.DEBUG),
    ]
    # raman = class_wrapper(logger, buffer_path)
    raman = WasatchDemo(mock_argv)

    if not raman.connect():
        return

    for _ in range(BROJ_MJERENJA):
        start_time = datetime.datetime.now()
        # NOTE: call demo.py
        raman.run()
        # asyncio.run(wrapper(logger, buffer_path))
        # NOTE: read external temperature from opc server
        temp = asyncio.run(temp_read(opc_ip))
        # NOTE: buffer + temp => file
        blend_in(writer, temp)
        end_time = datetime.datetime.now()

        time.sleep(calc_wait(start_time, end_time, VREMENSKI_ODMAK)*0.001)


if __name__ == "__main__":
    FORMAT = '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logging.getLogger("asyncua.client").setLevel(logging.WARNING)
    main()
