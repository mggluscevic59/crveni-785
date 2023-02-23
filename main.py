import logging
import asyncio
import datetime
import platform


from crystapp_04 import wrapper, temp_read, calc_wait, \
    GentleFileWriter, BROJ_MJERENJA, VREMENSKI_ODMAK


OPC_TEST = "178.238.237.121"
OPC_REAL = "192.168.0.118"


def blend_in(writer: GentleFileWriter, temp):
    with writer as file:
        with open(writer.buffer_path, "r", encoding="UTF-8") as buffer:
            spectra = buffer.readlines()[1].split(",")
            spectra[0] = datetime.datetime.now().strftime("%H:%M:%S")
            spectra[1] = temp
            logging.info("{0:7.2f}°C julabo t-1000".format(float(temp)))
            file.write(",".join([str(x) for x in spectra]))


async def main(log_level):
    """ Main loop program. Starts with file initialization. Every run: new file """
    writer = GentleFileWriter(".data/", ".buffer.csv")

    # buffer should be empty
    if writer.buffer_path.exists():
        writer.buffer_path.unlink()

    for i in range(BROJ_MJERENJA):
        start_time = end_time = task1 = tp_100 = None
        start_time = datetime.datetime.now()
        logging.debug("started measurement")

        # TP-100 from OPC UA server & Raman 785 from usb
        # task1 = asyncio.create_task(temp_read(f"opc.tcp://{OPC_TEST}:4840/freeopcua/server/"))
        task1 = asyncio.create_task(temp_read(f"opc.tcp://{OPC_REAL}:4840/freeopcua/server/"))
        await wrapper(log_level, writer.buffer_path)
        # await wrapper(log_level, writer.buffer_path, mock=True)

        # check buffer writed, then write TP-100 & spectra to data file
        if writer.buffer_path.exists():
            try:
                tp_100 = await task1
                tp_100 = tp_100 if isinstance(tp_100, float) else float(tp_100)
            except:
                logging.debug("OPC UA server unavailable. Exiting...")
                break
            blend_in(writer, tp_100)
        else:
            # wait for loggers, than exit
            await task1
            logging.debug("No data buffer for Raman. Exiting...")
            # logging.debug([writer.buffer_path.exists(), writer.buffer_path.absolute()])
            break
        end_time = datetime.datetime.now()
        logging.debug("ended measurement")

        logging.debug("measurement: {0}/{1}".format(i+1, BROJ_MJERENJA))
        if i != (BROJ_MJERENJA - 1):
            await asyncio.sleep(calc_wait(start_time, end_time, VREMENSKI_ODMAK))


if __name__ == "__main__":
    FORMAT = '%(asctime)s [0x%(thread)08x] %(name)s %(levelname)-8s %(message)s'

    if platform.system().lower()=="windows":
        raise Exception("Windows not supported!")

    # log level
    # logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    logging.getLogger("asyncua.client").setLevel(logging.WARNING)
    logging.getLogger("wasatch.FeatureIdentificationDevice").setLevel(logging.CRITICAL)

    asyncio.run(main(logging.INFO))
