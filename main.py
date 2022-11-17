#!/usr/bin/env python
import logging
import asyncio
import pathlib


from crystapp_04 import wrapper, temp_read, path_exists, set_filename


class GentleFileWriter:
    def __init__(self, folder, buffer):
        self.buffer_path = pathlib.Path(buffer)
        self.data_path = pathlib.Path(set_filename(folder=folder))

    def exists(self):
        return self.data_path.is_file()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def main(logger):
    # NOTE: call demo.py
    buffer_path = ".buffer.csv"
    # asyncio.run(wrapper(logger, buffer_path))

    # NOTE: read external temperature from opc server
    # NOTE: julabo i.p. address - 192.168.0.101
    # opc_ip = "192.168.0.118"
    # logging.info(asyncio.run(temp_read(logger, opc_ip)))
    temp = 100.00

    # NOTE: buffer + temp => file
    file = GentleFileWriter(".data/", buffer_path)
    logging.info(file.exists())

    # data_folder = ".data"
    # data_path = set_filename(folder=data_folder)
    # if not path_exists(data_path):
    #     open(data_path, "x", encoding="UTF-8")


if __name__ == "__main__":
    LOG_LEVEL, MESSAGE_FORMAT = logging.INFO, \
        '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # LOG_LEVEL, MESSAGE_FORMAT = logging.DEBUG, \
    #     '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=LOG_LEVEL, format=MESSAGE_FORMAT)
    main(LOG_LEVEL)
