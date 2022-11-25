#!/usr/bin/env python
import platform
import os
import logging
import subprocess


from asyncua import Client


INTEGRACIJSKO_VRIJEME = 500 # milisecond
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 3
VREMENSKI_ODMAK = 60000 # milisecond


async def wrapper(logger, outfile):
    # call demo_custom.py --help for list of parameters
    if platform.system().lower()=="windows":
        os.system(f"demo_custom.py --outfile={outfile} --max=1 --ascii-art \
            --integration-time-ms={INTEGRACIJSKO_VRIJEME} --log-level={logger} \
            --scans-to-average={BROJ_OCITANJA_ZA_INTERPOLACIJU}")
    else:
        command = [
            "./demo_custom.py",
            "--outfile",
            str(outfile),
            "--max",
            "1",
            "--integration-time-ms",
            str(INTEGRACIJSKO_VRIJEME),
            "--ascii-art",
            "--scans-to-average",
            str(BROJ_OCITANJA_ZA_INTERPOLACIJU),
            "--log-level",
            logging.getLevelName(logger)
        ]
        subprocess.call(command)


async def temp_read(logger, opc_ip):
    url = "opc.tcp://"+opc_ip+":4840/freeopcua/server/"
    temp = None

    async with Client(url=url) as client:
        # arbitrary namespace
        idx = await client.get_namespace_index(
            "urn:freeopcua:python:server"
        )
        temp = await (
            await client.nodes.objects.get_child(
                [f"{idx}:Devices", f"{idx}:JulaboMagio"]
                )
            ).call_method(f"{idx}:External_temperature", False)

    return temp
