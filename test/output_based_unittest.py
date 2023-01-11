import sys
sys.path.insert(1, ".")
import unittest
import logging


from wasatch.DeviceID import DeviceID
from wasatch.WasatchDevice import WasatchDevice
from crystapp_04.device import Device


class Output_Based(unittest.TestCase):
    def test_if_spectra_mock_working(self):
        id = DeviceID(label="MOCK:WP-00887:WP-00887-mock.json")
        logging.debug(id)
        device = WasatchDevice(device_id=id)
        device.connect()
        result1 = device.acquire_data()
        logging.debug(result1)
        device.disconnect()

        device = Device()
        result2 = device.spectra()

        self.assertEqual(result1, result2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
