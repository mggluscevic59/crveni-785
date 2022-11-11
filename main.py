#!/usr/bin/env python
import logging
import asyncio

from os.path import exists
from asyncua import Client
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
import wrapper


OPC_ADDR = "172.27.39.99"

def file_exists(path):
    if exists(".certs/key.pem"):
        return True
    return False


async def temp_read():
    cert = ".certs/certificate.pem"
    key = ".certs/key.pem"
    # # NOTE: init
    # client = Client(url=f"opc.tcp://{OPC_ADDR}:4840/freeopcua/server/")
    # await client.set_security(
    #     SecurityPolicyBasic256Sha256,
    #     certificate=".certs/certificate.pem",
    #     private_key=".certs/key.pem",
    # )

    # # NOTE: start
    # async with client:
    #     idx = await client.get_namespace_index(
    #         "urn:freeopcua:python:server"
    #     )
    #     logging.info(await client.nodes.objects.call_method(f"{idx}:External_temperature", False))


def main(logger):
    broj_mjerenja, vremenski_odmak, izlazna_mapa = 3, 0, ".data/"
    data_path = wrapper.path()
    buffer_path = ".buffer.csv"

    logging.info(data_path)
    # asyncio.run(wrapper.demo(logger))
    logging.info(asyncio.run(temp_read()))

    # for _ in range(broj_mjerenja):
    #     pass
        # if not os.path.exists(data_path):
        #     open(data_path, "x", encoding="UTF-8")
            # with open(data_path, "w", encoding="UTF-8") as file:
            #     file.write(table_header)

        # with open(buffer_path, "r", encoding="UTF-8") as buffer:
        #     table_header = buffer.readline()
        #     with open(data_path, "a", encoding="UTF-8") as file:
        #         logging.info(file.readable())


if __name__ == "__main__":
    LOG_LEVEL, MESSAGE_FORMAT = logging.INFO, \
        '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    # LOG_LEVEL, MESSAGE_FORMAT = logging.DEBUG, \
    #     '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=LOG_LEVEL, format=MESSAGE_FORMAT)
    main(LOG_LEVEL)
