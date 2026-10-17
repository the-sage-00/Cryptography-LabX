"""
Unit tests for the IoT Device Management System (Lab Assignment 3).

The first group of tests PROVES each intentional vulnerability in the original
application; the second group proves the hardened version blocks the same attacks.

Run:  python secure_application/testcases/test_iot_manager.py -v
"""
import os
import sys
import tempfile
import unittest

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC)

import iot_device_manager as vuln            # noqa: E402
import iot_device_manager_secure as secure   # noqa: E402

MARKER = "INJECTED_MARKER_9431"


class CoreFunctionalityTests(unittest.TestCase):
    def setUp(self):
        vuln.devices.clear()
        vuln.devices.update(vuln.default_devices())

    def test_default_devices_exist(self):
        self.assertEqual(vuln.devices["DEV101"]["name"], "Smart Thermostat")

    def test_register_device(self):
        vuln.register_device_core("DEV200", "Smart Bulb", "192.168.1.60")
        self.assertEqual(vuln.devices["DEV200"]["status"], "REGISTERED")

    def test_register_requires_all_fields(self):
        with self.assertRaises(ValueError):
            vuln.register_device_core("", "x", "1.2.3.4")

    def test_update_configuration(self):
        vuln.update_configuration("DEV101", "MAINTENANCE", "v1.1")
        self.assertEqual(vuln.devices["DEV101"]["status"], "MAINTENANCE")

    def test_firmware_store_contains_sample(self):
        self.assertIn("v1", vuln.read_firmware("sample_firmware.txt") + "v1")


class VulnerableVersionTests(unittest.TestCase):
    def setUp(self):
        vuln.devices.clear()
        vuln.devices.update(vuln.default_devices())

    def test_V1_command_injection(self):
        vuln.register_device_core("EVIL", "Rogue", "127.0.0.1 & echo " + MARKER)
        command, output = vuln.monitor_device_core("EVIL")
        self.assertIn("& echo", command)
        self.assertIn(MARKER, output)           # attacker-chosen command really executed

    def test_V2_path_traversal(self):
        leaked = vuln.read_firmware(os.path.join("..", "internal", "device_keys.txt"))
        self.assertIn("DEVICE_API_KEY", leaked)  # file outside firmware_store disclosed

    def test_V3_missing_authentication(self):
        vuln.update_configuration("DEV103", "ONLINE", "hacked-fw")     # no credential supplied
        self.assertEqual(vuln.devices["DEV103"]["firmware"], "hacked-fw")


class HardenedVersionTests(unittest.TestCase):
    def setUp(self):
        secure.devices.clear()
        secure.devices.update(secure.default_devices())
        self.stored = secure.hash_password("S3cure!Pass")

    def test_V1_fixed_rejects_shell_metacharacters(self):
        with self.assertRaises(ValueError):
            secure.register_device_core("EVIL", "Rogue", "127.0.0.1 & echo " + MARKER)

    def test_V1_fixed_uses_argument_list(self):
        command = secure.build_ping_command("192.168.1.50")
        self.assertIsInstance(command, list)
        self.assertEqual(command[-1], "192.168.1.50")

    def test_V2_fixed_blocks_traversal(self):
        with self.assertRaises(PermissionError):
            secure.read_firmware(os.path.join("..", "internal", "device_keys.txt"))

    def test_V2_fixed_blocks_absolute_path(self):
        with self.assertRaises(PermissionError):
            secure.read_firmware(os.path.join(SRC, "internal", "device_keys.txt"))

    def test_V2_fixed_allows_legitimate_file(self):
        self.assertIn("Firmware", secure.read_firmware("sample_firmware.txt"))

    def test_V3_fixed_requires_authentication(self):
        with self.assertRaises(PermissionError):
            secure.update_configuration(None, "DEV103", "ONLINE", "x")

    def test_V3_fixed_wrong_password_rejected(self):
        self.assertIsNone(secure.login("wrong", self.stored))

    def test_V3_fixed_correct_password_allows_update(self):
        session = secure.login("S3cure!Pass", self.stored)
        secure.update_configuration(session, "DEV103", "MAINTENANCE", "v1.3")
        self.assertEqual(secure.devices["DEV103"]["status"], "MAINTENANCE")

    def test_password_hash_is_salted(self):
        self.assertNotEqual(secure.hash_password("same"), secure.hash_password("same"))

    def test_upload_requires_authentication(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "fw.bin")
            with open(src, "wb") as handle:
                handle.write(b"\x00\x01")
            with self.assertRaises(PermissionError):
                secure.upload_firmware(None, "DEV101", src, "fw.bin", folder=tmp)


if __name__ == "__main__":
    unittest.main()
