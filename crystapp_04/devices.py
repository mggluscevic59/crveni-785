#!/usr/bin/env python
# import platform
# import os
import logging
import subprocess
import asyncio


from asyncua import Client


INTEGRACIJSKO_VRIJEME = 500 # milisecond
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 60
VREMENSKI_ODMAK = 30000 # milisecond


async def wrapper(log_level, outfile, mock=False):
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
        logging.getLevelName(log_level)
    ]
    if mock:
        command.append("--use-mock")
    subprocess.call(command)
    # estimated time to finish julabo
    await asyncio.sleep(0.001)


async def temp_read(url):
    client = Client(url=url)

    try:
        await client.connect()
    except asyncio.exceptions.TimeoutError:
        logging.warning("No opc server present!")
        return
    else:
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
