#!/usr/bin/env python
import platform
import os
import logging
import subprocess
import sys


from asyncua import Client
from demo_custom import WasatchDemo


log = logging.getLogger(__name__)


async def temp_read(opc_ip):
    url = "opc.tcp://"+opc_ip+":4840/freeopcua/server/"
    temp = None

    async with Client(url=url) as client:
        log.debug("Start reading Julabo t-1000")
        # arbitrary namespace
        idx = await client.get_namespace_index(
            "urn:freeopcua:python:server"
        )
        temp = await (
            await client.nodes.objects.get_child(
                [f"{idx}:Devices", f"{idx}:JulaboMagio"]
                )
            ).call_method(f"{idx}:External_temperature", False)
        log.debug("temperature has been red!")
        log.info(temp)

    return temp
