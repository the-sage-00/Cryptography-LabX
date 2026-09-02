"""
Test cases for IoT Device Management System
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from iot_device_manager import devices, setup_application


class TestIoTDeviceManager(unittest.TestCase):

    def setUp(self):
        setup_application()

    def test_default_devices_exist(self):
        self.assertIn("DEV101", devices)
        self.assertEqual(devices["DEV101"]["name"], "Smart Thermostat")

    def test_firmware_directory_created(self):
        firmware_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "firmware_store"))
        self.assertTrue(os.path.exists(firmware_dir))


if __name__ == "__main__":
    unittest.main()
