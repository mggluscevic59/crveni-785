#!/usr/bin/env python
################################################################################
#                                   demo_cutom.py                              #
################################################################################
#                                                                              #
#  DESCRIPTION:  Simple cmd-line demo to confirm that Wasatch.PY is working    #
#                and can connect to and control a spectrometer.                #
#                                                                              #
#  ENVIRONMENT:  (if using Miniconda3)                                         #
#                $ rm -f environment.yml                                       #
#                $ ln -s environments/conda-linux.yml  (or macos, etc)         #
#                $ conda env create -n wasatch3                                #
#                $ conda activate wasatch3                                     #
#  INVOCATION:                                                                 #
#                $ python -u demo.py                                           #
#                                                                              #
################################################################################
# import os
import re
import sys
import time
import numpy
import signal
# import psutil
import logging
import datetime
import argparse
import wasatch


from wasatch import utils
from wasatch import applog
from wasatch.WasatchBus           import WasatchBus
from wasatch.OceanDevice          import OceanDevice
from wasatch.WasatchDevice        import WasatchDevice
from wasatch.WasatchDeviceWrapper import WasatchDeviceWrapper
from wasatch.RealUSBDevice        import RealUSBDevice
from wasatch.DeviceID             import DeviceID


log = logging.getLogger(__name__)


class WasatchDemo(object):
    ############################################################################
    #                                                                          #
    #                               Lifecycle                                  #
    #                                                                          #
    ############################################################################
    def __init__(self, argv=None):
        self.bus     = None
        self.device  = None
        self.logger  = None
        self.outfile = None
        self.exiting = False
        self.reading_count = None
        self._laser = False

        self.args = self.parse_args(argv)

        self.logger = applog.MainLogger(self.args.log_level, logfile=".wasatch_applog.txt")
        log.info("Wasatch.PY version %s", wasatch.__version__)

    @property
    def laser(self):
        return self._laser

    @laser.setter
    def laser(self, value:bool):
        self.device.hardware.set_laser_enable(value)
        self._laser = value

    ############################################################################
    #                                                                          #
    #                             Command-Line Args                            #
    #                                                                          #
    ############################################################################
    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description="Simple demo to acquire spectra from command-line interface")
        parser.add_argument("--log-level",           type=str, default="INFO", help="logging level [DEBUG,INFO,WARNING,ERROR,CRITICAL]")
        parser.add_argument("--integration-time-ms", type=int, default=10,     help="integration time (ms, default 10)")
        parser.add_argument("--scans-to-average",    type=int, default=1,      help="scans to average (default 1)")
        parser.add_argument("--boxcar-half-width",   type=int, default=0,      help="boxcar half-width (default 0)")
        # parser.add_argument("--delay-ms",            type=int, default=1000,   help="delay between integrations (ms, default 1000)")
        parser.add_argument("--outfile",             type=str, default=None,   help="output filename (e.g. path/to/spectra.csv)")
        parser.add_argument("--max",                 type=int, default=0,      help="max spectra to acquire (default 0, unlimited)")
        parser.add_argument("--use-mock",            action="store_true",      help="use virtual device for debugging")
        parser.add_argument("--non-blocking",        action="store_true",      help="non-blocking USB interface (WasatchDeviceWrapper instead of WasatchDevice)")
        parser.add_argument("--ascii-art",           action="store_true",      help="graph spectra in ASCII")
        parser.add_argument("--version",             action="store_true",      help="display Wasatch.PY version and exit")

        # parse argv into dict
        args = parser.parse_args(argv[1:])
        if args.version:
            log.info("Wasatch.PY %s", wasatch.__version__)
            sys.exit(0)

        # normalize log level
        args.log_level = args.log_level.upper()
        if not re.match("^(DEBUG|INFO|ERROR|WARNING|CRITICAL)$", args.log_level):
            log.info("Invalid log level: %s (defaulting to INFO)", args.log_level)
            args.log_level = "INFO"

        return args
        
    ############################################################################
    #                                                                          #
    #                              USB Devices                                 #
    #                                                                          #
    ############################################################################

    def connect(self):
        """ If the current device is disconnected, and there is a new device, 
            attempt to connect to it. """

        # if we're already connected, nevermind
        if self.device is not None:
            return

        # lazy-load a USB bus
        if self.bus is None:
            log.debug("instantiating WasatchBus")
            self.bus = WasatchBus(use_sim = False)

        if not self.bus.device_ids:
            log.warning("No Wasatch USB spectrometers found.")
            if self.args.use_mock:
                log.info("Using mock up device.")
                device_id = DeviceID(label="MOCK:WP-00887:WP-00887-mock.json")
                log.debug(hex(device_id.vid))
            else:
                return
        else:
            device_id = self.bus.device_ids[0]
            device_id.device_type = RealUSBDevice(device_id)

        log.debug("connect: trying to connect to %s", device_id)

        if self.args.non_blocking:
            # this is still buggy on MacOS
            log.debug("instantiating WasatchDeviceWrapper (non-blocking)")
            device = WasatchDeviceWrapper(
                device_id = device_id,
                # log_queue = self.logger.log_queue,
                log_level = self.args.log_level)
        else:
            log.debug("instantiating WasatchDevice (blocking)")
            if device_id.vid == 0x24aa or device_id.vid == int(str(hash(device_id.name))):
                device = WasatchDevice(device_id)
            else:
                log.debug("Instatiating Ocean device")
                device = OceanDevice(device_id)

        o_k = device.connect()
        if not o_k:
            log.critical("connect: can't connect to %s", device_id)
            return

        log.debug("connect: device connected")

        self.device = device
        self.laser = device.hardware.get_laser_enabled()
        self.reading_count = 0

        return device

    ############################################################################
    #                                                                          #
    #                               Run-Time Loop                              #
    #                                                                          #
    ############################################################################

    def run(self):
        log.info("Wasatch.PY %s Demo", wasatch.__version__)

        # apply initial settings
        self.device.change_setting("integration_time_ms", self.args.integration_time_ms)
        self.device.change_setting("scans_to_average", self.args.scans_to_average)
        self.device.change_setting("detector_tec_enable", True)
        # self.device.change_setting("acquisition_laser_trigger_enable", True)

        # initialize outfile if one was specified
        if self.args.outfile:
            try:
                self.outfile = open(self.args.outfile, "w", encoding="utf-8")
                self.outfile.write("time,temp,%s\n" % ",".join(format(x, ".2f") for x in self.device.settings.wavelengths))
            except:
                log.error("Error initializing %s", self.args.outfile)
                self.outfile = None

        # read spectra until user presses Control-Break
        while not self.exiting:
            # only place where laser is turned on & awaited (sleep)
            self.laser = True
            try:
                time.sleep(10)
                # threading.Event().wait(10)
            except:
                # log.critical("WasatchDemo.run sleep() caught an exception", exc_info=1)
                self.exiting = True
            self.attempt_reading()
            self.laser = False

            # TODO: move to main module
            if self.args.max > 0 and self.reading_count >= self.args.max:
                log.debug("max spectra reached, exiting")
                self.exiting = True

        log.debug("WasatchDemo.run exiting")

    def laser_toggle(self):
        self.laser = not self.laser

    def attempt_reading(self):
        try:
            reading_response = self.acquire_reading()
        except Exception as exc:
            log.critical("attempt_reading caught exception", exc_info=1)
            self.exiting = True
            return

        if isinstance(reading_response.data, bool):
            if reading_response.data:
                log.debug("received poison-pill, exiting")
                self.exiting = True
                return
            else:
                log.debug("no reading available")
                return

        if reading_response.data.failure:
            self.exiting = True
            return

        self.process_reading(reading_response.data)

    def acquire_reading(self):
        # We want the demo to effectively block on new scans, so keep
        # polling the subprocess until a reading is ready.  In other apps,
        # we could do other things (like respond to GUI events) if 
        # device.acquire_data() was None (meaning the next spectrum wasn't
        # yet ready).
        while True:
            reading = self.device.acquire_data()
            if reading is None:
                log.debug("waiting on next reading")
            else:
                return reading

    def process_reading(self, reading):
        if self.args.scans_to_average > 1 and not reading.averaged:
            return

        self.reading_count += 1

        if self.args.boxcar_half_width > 0:
            spectrum = utils.apply_boxcar(reading.spectrum, self.args.boxcar_half_width)
        else:
            spectrum = reading.spectrum

        if self.args.ascii_art:
            log.info("\n"+"\n".join(wasatch.utils.ascii_spectrum(spectrum, rows=20, cols=80, x_axis=self.device.settings.wavelengths, x_unit="nm")))
            # log.info("\n".join(wasatch.utils.ascii_spectrum(spectrum, rows=20, cols=80, x_axis=self.device.settings.wavelengths, x_unit="nm")))
        else:
            spectrum_min = numpy.amin(spectrum)
            spectrum_max = numpy.amax(spectrum)
            spectrum_avg = numpy.mean(spectrum)
            spectrum_std = numpy.std (spectrum)

            log.info("Reading: %4d  Detector: %5.2f degC  Min: %8.2f  Max: %8.2f  Avg: %8.2f  StdDev: %8.2f  Memory: %11d" % (
                self.reading_count,
                reading.detector_temperature_degC,
                spectrum_min,
                spectrum_max,
                spectrum_avg,
                spectrum_std))
            log.debug("%s", str(reading))

        if self.outfile:
            self.outfile.write("%s,%.2f,%s\n" % (datetime.datetime.now(),
                                                 reading.detector_temperature_degC,
                                                 ",".join(format(x, ".2f") for x in spectrum)))

################################################################################
# main()
################################################################################

def signal_handler(signal, frame):
    log.info('\rInterrupted by Ctrl-C...shutting down', end=' ')
    clean_shutdown()

def clean_shutdown():
    log.debug("Exiting")

    # precaution! already covered by disconnect
    # if demo.laser:
    #     demo.laser = False

    if demo:
        if demo.args and demo.args.non_blocking and demo.device:
            log.debug("closing background thread")
            demo.device.disconnect()

        if demo.logger:
            log.debug("closing logger")
            log.debug(None)
            demo.logger.close()
            time.sleep(1)
            applog.explicit_log_close()
    sys.exit()

demo = None
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    demo = WasatchDemo(sys.argv)
    if demo.connect():
        # Note that on Windows, Control-Break (SIGBREAK) differs from
        # Control-C (SIGINT); see https://stackoverflow.com/a/1364199
        log.debug("Press Control-Break to interrupt...")
        demo.run()

    clean_shutdown()
