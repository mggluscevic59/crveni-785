#!/usr/bin/env python
import logging
import asyncio
import os
# import datetime
import platform
import subprocess


from asyncua import Client
# import crystapp_04
# from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256


# OPC_ADDR = "172.27.39.99"
INTEGRACIJSKO_VRIJEME = 10
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 3
VREMENSKI_ODMAK = 0
# IZLAZNA_MAPA = ".data/"


async def wrapper(logger, outfile):
    # call demo_custom.py --help for list of parameters
    if platform.system().lower()=="windows":
        os.system(f"demo_custom.py --integration-time-ms={INTEGRACIJSKO_VRIJEME} \
            --scans-to-average={BROJ_OCITANJA_ZA_INTERPOLACIJU} --max=1 \
                --delay-ms={VREMENSKI_ODMAK} --outfile={outfile} \
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
            str(outfile),
            "--ascii-art",
            "--log-level",
            logging.getLevelName(logger)
        ]
        subprocess.call(command)


async def temp_read(logger, opc_ip):
    url = "opc.tcp://"+opc_ip+":4840/freeopcua/server/"
    temp = None

    async with Client(url=url) as client:
        idx = await client.get_namespace_index(
            "urn:freeopcua:python:server"
        )
        folder = await client.nodes.objects.get_child(f"{idx}:Devices")
        device = await folder.get_child(f"{idx}:JulaboMagio")
        temp = await device.call_method(f"{idx}:External_temperature", False)
    
    return temp


def main(logger):
    # NOTE: call demo.py
    buffer_path = ".buffer.csv"
    asyncio.run(wrapper(logger, buffer_path))

    opc_ip = "192.168.0.118"
    logging.info(asyncio.run(temp_read(logger, opc_ip)))

    # broj_mjerenja, vremenski_odmak, izlazna_mapa = 3, 0, ".data/"
    # data_path = crystapp_04.set_filename(folder=IZLAZNA_MAPA)
    
    # jul_1 = julabo.JulaboMS(julabo.connection_for_url("tcp://178.238.237.121:5050"))
    # logging.info(data_path)
    
    # logging.info(asyncio.run(get_ms(jul_1, "identification")))
    # logging.info(asyncio.run(get_ms(jul_1, "external_temperature")))
    # for _ in range(broj_mjerenja):
        # pass

    # logging.info(data_path)

    # for _ in range(broj_mjerenja):
    #     pass
    # if not crystapp_04.path_exists(data_path):
        # open(data_path, "x", encoding="UTF-8")

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
