#!/usr/bin/env python
import platform
import os
import logging
import subprocess
import asyncio


from asyncua import Client


INTEGRACIJSKO_VRIJEME = 500 # milisecond
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 10
VREMENSKI_ODMAK = 30000 # milisecond


async def wrapper(logger, outfile):
    # call demo_custom.py --help for list of parameters
    if platform.system().lower()=="windows":
        os.system(f"demo_custom.py --outfile={outfile} --max=1 --ascii-art \
            --integration-time-ms={INTEGRACIJSKO_VRIJEME} \
            --scans-to-average={BROJ_OCITANJA_ZA_INTERPOLACIJU} \
            --log-level={logging.getLevelName(logger)}")
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
    # estimated time to finish julabo
    await asyncio.sleep(0.001)


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
    # estimated time to finish raman
    await asyncio.sleep(0.001)

    return temp
