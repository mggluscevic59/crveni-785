#!/usr/bin/env python
import logging
import asyncio
import time


from crystapp_04 import wrapper, temp_read, GentleFileWriter, BROJ_MJERENJA


def blend_in(buffer_path, temp):
    with GentleFileWriter(".data/", buffer_path) as file:
        with open(buffer_path, "r", encoding="UTF-8") as buffer:
            spectra = buffer.readlines()[1].split(",")
            spectra[1] = temp
            file.write(",".join([str(x) for x in spectra]))


def main(logger):
    # NOTE: julabo i.p. address - 192.168.0.101
    buffer_path, opc_ip = ".buffer.csv", "192.168.0.118"
    # logging.info(asyncio.run(temp_read(logger, opc_ip)))
    # temp = "100.00"

    for _ in range(BROJ_MJERENJA):
        # NOTE: call demo.py
        asyncio.run(wrapper(logger, buffer_path))
        # NOTE: read external temperature from opc server
        temp = asyncio.run(temp_read(logger, opc_ip))
        # NOTE: buffer + temp => file
        blend_in(buffer_path, temp)
        time.sleep(1)


if __name__ == "__main__":
    LOG_LEVEL, MESSAGE_FORMAT = logging.INFO, \
        '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # LOG_LEVEL, MESSAGE_FORMAT = logging.DEBUG, \
    #     '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=LOG_LEVEL, format=MESSAGE_FORMAT)
    main(LOG_LEVEL)
