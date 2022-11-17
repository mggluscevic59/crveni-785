#!/usr/bin/env python
import logging
import asyncio


from crystapp_04 import wrapper, temp_read, GentleFileWriter


def main(logger):
    # NOTE: call demo.py
    buffer_path = ".buffer.csv"
    asyncio.run(wrapper(logger, buffer_path))

    # NOTE: read external temperature from opc server
    # NOTE: julabo i.p. address - 192.168.0.101
    opc_ip = "192.168.0.118"
    # logging.info(asyncio.run(temp_read(logger, opc_ip)))
    temp = asyncio.run(temp_read(logger, opc_ip))
    # temp = "100.00"

    # NOTE: buffer + temp => file
    writer = GentleFileWriter(".data/", buffer_path)
    with writer as file:
        with open(buffer_path, "r", encoding="UTF-8") as buffer:
            spectra = buffer.readlines()[1].split(",")
            spectra[1] = temp
            file.write(",".join([str(x) for x in spectra]))
            # file.write(buffer.readlines()[1])


if __name__ == "__main__":
    LOG_LEVEL, MESSAGE_FORMAT = logging.INFO, \
        '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # LOG_LEVEL, MESSAGE_FORMAT = logging.DEBUG, \
    #     '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=LOG_LEVEL, format=MESSAGE_FORMAT)
    main(LOG_LEVEL)
