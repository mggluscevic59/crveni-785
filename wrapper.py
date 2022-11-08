#!/usr/bin/env python
import os
import datetime
import logging
import asyncio

"""
    ulazni podaci
"""
INTEGRACIJSKO_VRIJEME = 10
BROJ_OCITANJA_ZA_INTERPOLACIJU = 1
BROJ_MJERENJA = 3           # \
VREMENSKI_ODMAK = 0         #  | postaviti u glavnom programu!
IZLAZNA_MAPA = ".data/"     # /



"""
    kôd
"""
def main(logger):
    putanja = path()
    print(putanja)
    os.system(f"demo.py --integration-time-ms={INTEGRACIJSKO_VRIJEME} --scans-to-average={BROJ_OCITANJA_ZA_INTERPOLACIJU} --max={BROJ_MJERENJA} --delay-ms={VREMENSKI_ODMAK} --outfile={putanja} --ascii-art --log-level={logger}")

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
    return foo_path

async def demo(logger):
    os.system(f"demo.py --integration-time-ms={INTEGRACIJSKO_VRIJEME} --scans-to-average={BROJ_OCITANJA_ZA_INTERPOLACIJU} --max=1 --outfile=.buffer.csv --ascii-art --log-level={logger}")

if __name__ == "__main__":
    log_level = "WARNING"
    logging.basicConfig(level=getattr(logging, log_level))
    main(log_level)
