#!/usr/bin/env python
import logging
import asyncio
import wrapper


def main(logger):
    broj_mjerenja, vremenski_odmak, izlazna_mapa = 3, 0, ".data/"
    putanja = wrapper.path()
    logging.info(putanja)
    asyncio.run(wrapper.demo(logger))


if __name__ == "__main__":
    log_level = logging.DEBUG
    message_format = u'%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=log_level, format=message_format)
    main(log_level)
