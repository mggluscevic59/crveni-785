#!/usr/bin/env python
import platform
import os
import logging
import subprocess


from asyncua import Client


INTEGRACIJSKO_VRIJEME = 10
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 3
VREMENSKI_ODMAK = 0


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
