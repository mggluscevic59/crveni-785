#!/usr/bin/env python
import logging
import asyncio
import wrapper

def main(logger):
    putanja = wrapper.path()
    logging.info(putanja)

if __name__ == "__main__":
    # log_level = "WARNING"
    log_level = "INFO"
    logging.basicConfig(level=getattr(logging, log_level))
    main(log_level)
