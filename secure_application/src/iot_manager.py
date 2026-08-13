import os
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "devices.json"
FIRMWARE_DIR = BASE_DIR / "firmware"

FIRMWARE_DIR.mkdir(exist_ok=True)


def load_devices():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_devices(devices):
    with open(DATA_FILE, "w") as f:
        json.dump(devices, f, indent=4)


def register_device():
    devices = load_devices()

    device_id = input("Enter device ID: ")
    device_name = input("Enter device name: ")
    ip_address = input("Enter device IP address: ")

    devices[device_id] = {
        "name": device_name,
        "ip": ip_address,
        "status": "Registered",
        "configuration": {}
    }

    save_devices(devices)

    print("Device registered successfully.")


def view_devices():
    devices = load_devices()

    if not devices:
        print("No devices registered.")
        return

    for device_id, device in devices.items():
        print("\nDevice ID:", device_id)
        print("Name:", device["name"])
        print("IP:", device["ip"])
        print("Status:", device["status"])


def check_status():
    devices = load_devices()

    device_id = input("Enter device ID: ")

    if device_id not in devices:
        print("Device not found.")
        return

    ip_address = input("Enter device IP address: ")

    # VULNERABILITY 1: Command Injection
    command = "ping -n 1 " + ip_address
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print(result.stdout)


def upload_firmware():
    filename = input("Enter firmware filename: ")

    # VULNERABILITY 2: Path Traversal
    firmware_path = FIRMWARE_DIR / filename

    firmware_content = input("Enter firmware content: ")

    with open(firmware_path, "w") as f:
        f.write(firmware_content)

    print("Firmware uploaded successfully.")
    print("Saved to:", firmware_path)


def change_configuration():
    devices = load_devices()

    device_id = input("Enter device ID: ")

    if device_id not in devices:
        print("Device not found.")
        return

    # VULNERABILITY 3: Missing Authentication
    parameter = input("Enter configuration parameter: ")
    value = input("Enter configuration value: ")

    devices[device_id]["configuration"][parameter] = value

    save_devices(devices)

    print("Configuration updated successfully.")


def main():
    while True:
        print("\n===== IoT Device Management =====")
        print("1. Register Device")
        print("2. View Devices")
        print("3. Check Device Status")
        print("4. Upload Firmware")
        print("5. Change Configuration")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_device()

        elif choice == "2":
            view_devices()

        elif choice == "3":
            check_status()

        elif choice == "4":
            upload_firmware()

        elif choice == "5":
            change_configuration()

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()