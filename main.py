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
    # log_level = "WARNING"
    log_level = "INFO"
    logging.basicConfig(level=getattr(logging, log_level))
    main(log_level)
