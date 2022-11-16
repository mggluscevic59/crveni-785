#!/usr/bin/env python
import logging
import asyncio


from crystapp_04 import wrapper, temp_read


def main(logger):
    # NOTE: call demo.py
    buffer_path = ".buffer.csv"
    asyncio.run(wrapper(logger, buffer_path))

    opc_ip = "192.168.0.118"
    logging.info(asyncio.run(temp_read(logger, opc_ip)))


if __name__ == "__main__":
    LOG_LEVEL, MESSAGE_FORMAT = logging.INFO, \
        '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # LOG_LEVEL, MESSAGE_FORMAT = logging.DEBUG, \
    #     '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=LOG_LEVEL, format=MESSAGE_FORMAT)
    main(LOG_LEVEL)
