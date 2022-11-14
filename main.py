#!/usr/bin/env python
import logging
import asyncio
import os
import datetime
import platform
import subprocess


from asyncua import Client
# from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256


OPC_ADDR = "172.27.39.99"
INTEGRACIJSKO_VRIJEME = 10
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 3
VREMENSKI_ODMAK = 0
IZLAZNA_MAPA = ".data/"


def path(enum=True, timestamp=True):
    foo_path = IZLAZNA_MAPA

    if timestamp:
        foo_path += datetime.datetime.now().strftime('%Y_%m_%d')
    if enum:
        counter = 1
        while os.path.exists(foo_path+"-"+str(counter)+".csv"):
            counter += 1
        foo_path += "-" + str(counter)
    foo_path += ".csv"
    return 


async def wrapper(logger):
    # call demo_custom.py --help for list of parameters
    if platform.system().lower()=="windows":
        os.system(f"demo_custom.py --integration-time-ms={INTEGRACIJSKO_VRIJEME} \
            --scans-to-average={BROJ_OCITANJA_ZA_INTERPOLACIJU} --max=1 \
                --delay-ms={VREMENSKI_ODMAK} --outfile='.buffer.csv' \
                    --ascii-art --log-level={logger}")
    else:
        command = [
            "./demo_custom.py",
            "--integration-time-ms",
            str(INTEGRACIJSKO_VRIJEME),
            "--scans-to-average",
            str(BROJ_OCITANJA_ZA_INTERPOLACIJU),
            "--max",
            "1",
            "--outfile",
            ".buffer.csv",
            "--ascii-art",
            "--log-level",
            logging.getLevelName(logger)
        ]
        subprocess.call(command)


async def temp_read():
    cert = ".certs/certificate.pem"
    key = ".certs/key.pem"
    # NOTE: init
    client = Client(url=f"opc.tcp://{OPC_ADDR}:4840/freeopcua/server/")
    # await client.set_security(
    #     SecurityPolicyBasic256Sha256,
    #     certificate=".certs/certificate.pem",
    #     private_key=".certs/key.pem",
    # )

    # NOTE: start
    # async with client:
    #     idx = await client.get_namespace_index(
    #         "urn:freeopcua:python:server"
    #     )
    #     logging.info(await client.nodes.objects.call_method(f"{idx}:External_temperature", False))


def main(logger):
    broj_mjerenja, vremenski_odmak, izlazna_mapa = 3, 0, ".data/"
    # data_path = wrapper.path()
    buffer_path = ".buffer.csv"
    # jul_1 = julabo.JulaboMS(julabo.connection_for_url("tcp://178.238.237.121:5050"))
    # logging.info(data_path)
    asyncio.run(wrapper(logger))
    # logging.info(asyncio.run(get_ms(jul_1, "identification")))
    # logging.info(asyncio.run(get_ms(jul_1, "external_temperature")))
    for _ in range(broj_mjerenja):
        pass

    # logging.info(data_path)
    # logging.info(asyncio.run(temp_read()))

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
