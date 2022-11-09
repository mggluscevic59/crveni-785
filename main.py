#!/usr/bin/env python
import logging
import asyncio
import julabo
import os
import wrapper


async def get_ms(jul, command):
    result = None
    await jul.protocol.conn.open()
    result = await getattr(jul, command)()
    await jul.protocol.conn.close()

    return result


def main(logger):
    broj_mjerenja, vremenski_odmak, izlazna_mapa = 3, 0, ".data/"
    data_path = wrapper.path()
    buffer_path = ".buffer.csv"
    jul_1 = julabo.JulaboMS(julabo.connection_for_url("tcp://178.238.237.121:5050"))
    logging.info(data_path)
    asyncio.run(wrapper.demo(logger))
    logging.info(asyncio.run(get_ms(jul_1, "identification")))
    logging.info(asyncio.run(get_ms(jul_1, "external_temperature")))
    for _ in range(broj_mjerenja):
        pass
        # if not os.path.exists(data_path):
        #     open(data_path, "x", encoding="UTF-8")
            # with open(data_path, "w", encoding="UTF-8") as file:
            #     file.write(table_header)

        # with open(buffer_path, "r", encoding="UTF-8") as buffer:
        #     table_header = buffer.readline()
        #     with open(data_path, "a", encoding="UTF-8") as file:
        #         logging.info(file.readable())


if __name__ == "__main__":
    LOG_LEVEL, MESSAGE_FORMAT = logging.INFO, '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # LOG_LEVEL, MESSAGE_FORMAT = logging.DEBUG, '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=LOG_LEVEL, format=MESSAGE_FORMAT)
    main(LOG_LEVEL)
