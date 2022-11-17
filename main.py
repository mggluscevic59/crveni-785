#!/usr/bin/env python
import logging
import asyncio
import pathlib


from crystapp_04 import wrapper, temp_read, path_exists, set_filename


class GentleFileWriter:
    def __init__(self, folder, buffer, filename=None):
        self.buffer_path = pathlib.Path(buffer)
        if filename is None:
            self.data_path = pathlib.Path(set_filename(folder=folder))
        else:
            self.data_path = pathlib.Path(folder+filename)
        self.file = None

    def exists(self):
        return self.data_path.is_file()

    def _add_header(self):
        if not self.exists():
            with open(self.data_path, "w+", encoding="UTF-8") as file:
                with open(self.buffer_path, "r", encoding="UTF-8") as buffer:
                    file.write(buffer.readline())
        else:
            if not self.header_is_ok():
                raise BufferError("New data colides old data!")

    def _delete(self):
        self.data_path.unlink()

    def header_is_ok(self):
        with open(self.data_path, "r", encoding="UTF-8") as file:
                with open(self.buffer_path, "r", encoding="UTF-8") as buffer:
                    if file.readline() == buffer.readline():
                        return True
                    return False

    def is_almost_empty(self):
        with open(self.data_path, "r", encoding="UTF-8") as file:
            # NOTE: read header first, that is the "almost" empty part
            file.readline()
            if not file.readline().strip():
                return True
            return False

    def __enter__(self):
        self._add_header()
        self.file = open(self.data_path, "a", encoding="UTF-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        if self.is_almost_empty():
            self._delete()


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
    writer = GentleFileWriter(".data/", buffer_path)
    with writer as file:
        # file.write("Hello")
    # logging.info(file.create())
    # with GentleFileWriter(".data/", buffer_path) as file:
    #     logging.info(file)

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
