"""
Lab Assignment 3 - IoT Device Management System (INTENTIONALLY VULNERABLE VERSION)

Course   : Cryptography Laboratory (22CPP307)
Group    : 10  (Application 10 = IoT Device Management)
Language : Python 3        SAST tool: Semgrep

Core functionalities
    1. Smart device registration
    2. Device status monitoring
    3. Firmware upload / view
    4. Configuration management
    5. Device listing

Intentional vulnerabilities (exactly three, as required by the assignment)
    V1  Command Injection      -> build_ping_command() / monitor_device()
    V2  Path Traversal         -> read_firmware()
    V3  Missing Authentication -> upload_firmware() / update_configuration()
                                  (privileged actions never check who the caller is)

The hardened counterpart is in iot_device_manager_secure.py.
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_FOLDER = os.path.join(BASE_DIR, "firmware_store")


def default_devices():
    return {
        "DEV101": {"name": "Smart Thermostat", "ip": "192.168.1.50", "status": "ONLINE",  "firmware": "v1.0"},
        "DEV102": {"name": "Security Camera",  "ip": "192.168.1.51", "status": "ONLINE",  "firmware": "v2.0"},
        "DEV103": {"name": "Smart Door Lock",  "ip": "192.168.1.52", "status": "OFFLINE", "firmware": "v1.2"},
    }


devices = default_devices()


# ----------------------------------------------------------------------------
# 1. Device registration
# ----------------------------------------------------------------------------
def register_device_core(device_id, name, ip):
    """Register a device. NOTE: ip is stored without any validation."""
    if not device_id or not name or not ip:
        raise ValueError("All fields are required")
    devices[device_id] = {"name": name, "ip": ip, "status": "REGISTERED", "firmware": "v1.0"}


# ----------------------------------------------------------------------------
# 2. Device status monitoring   (V1: COMMAND INJECTION)
# ----------------------------------------------------------------------------
def build_ping_command(ip):
    # VULNERABILITY V1: user-controlled text is concatenated into a shell command line.
    if os.name == "nt":
        return "ping -n 1 " + ip
    return "ping -c 1 " + ip


def monitor_device_core(device_id):
    ip = devices[device_id]["ip"]
    command = build_ping_command(ip)
    # VULNERABILITY V1: shell=True lets metacharacters (& ; |) start extra commands.
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return command, result.stdout + result.stderr


# ----------------------------------------------------------------------------
# 3. Firmware management        (V2: PATH TRAVERSAL, V3: MISSING AUTHENTICATION)
# ----------------------------------------------------------------------------
def read_firmware(filename, folder=FIRMWARE_FOLDER):
    # VULNERABILITY V2: filename is joined to the folder with no validation, so
    # "../internal/device_keys.txt" escapes the firmware directory.
    file_path = os.path.join(folder, filename)
    with open(file_path, "r") as handle:
        return handle.read()


def upload_firmware(device_id, source_file, new_name, folder=FIRMWARE_FOLDER):
    # VULNERABILITY V3: no authentication / authorisation before a privileged action.
    destination = os.path.join(folder, new_name)
    with open(source_file, "rb") as src:
        data = src.read()
    with open(destination, "wb") as dst:
        dst.write(data)
    devices[device_id]["firmware"] = new_name


# ----------------------------------------------------------------------------
# 4. Configuration management   (V3: MISSING AUTHENTICATION)
# ----------------------------------------------------------------------------
def update_configuration(device_id, status=None, firmware=None):
    # VULNERABILITY V3: anybody who can run the menu may reconfigure any device.
    if status:
        devices[device_id]["status"] = status
    if firmware:
        devices[device_id]["firmware"] = firmware


# ----------------------------------------------------------------------------
# Console user interface
# ----------------------------------------------------------------------------
def setup_application():
    os.makedirs(FIRMWARE_FOLDER, exist_ok=True)
    sample = os.path.join(FIRMWARE_FOLDER, "sample_firmware.txt")
    if not os.path.exists(sample):
        with open(sample, "w") as handle:
            handle.write("Sample IoT Firmware\nVersion: 1.0\nDevice Type: Smart Device\n")


def register_device():
    print("\n================================\n        REGISTER DEVICE\n================================")
    device_id = input("Enter Device ID: ").strip()
    name = input("Enter Device Name: ").strip()
    ip = input("Enter IP Address: ").strip()
    try:
        register_device_core(device_id, name, ip)
        print("\n[+] Device registered successfully!")
    except ValueError as error:
        print("\n[!]", error)


def list_devices():
    print("\n================================\n       REGISTERED DEVICES\n================================")
    for dev_id, info in devices.items():
        print(f"{dev_id} | {info['name']:<18} | {info['ip']:<15} | {info['status']:<10} | FW {info['firmware']}")


def monitor_device():
    print("\n================================\n        DEVICE MONITORING\n================================")
    device_id = input("Enter Device ID: ").strip()
    if device_id not in devices:
        print("\n[!] Device not found.")
        return
    command, output = monitor_device_core(device_id)
    print("\nExecuting:", command)
    print("\n--- Ping Result ---")
    print(output[:500])


def firmware_management():
    while True:
        print("\n================================\n       FIRMWARE MANAGEMENT\n================================")
        print("1. View Firmware File\n2. Upload Firmware\n3. Back")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            filename = input("Enter firmware filename: ").strip()
            try:
                print("\n--- File Contents ---")
                print(read_firmware(filename))
                print("---------------------")
            except OSError as error:
                print("\n[!] Error:", error)
        elif choice == "2":
            device_id = input("Enter Device ID: ").strip()
            if device_id not in devices:
                print("\n[!] Device not found.")
                continue
            source = input("Enter path of firmware file: ").strip()
            name = input("Enter name for uploaded firmware: ").strip()
            try:
                upload_firmware(device_id, source, name)
                print("\n[+] Firmware uploaded successfully!")
            except OSError as error:
                print("\n[!] Error:", error)
        elif choice == "3":
            break
        else:
            print("\n[!] Invalid choice.")


def configuration_management():
    print("\n================================\n      UPDATE CONFIGURATION\n================================")
    device_id = input("Enter Device ID: ").strip()
    if device_id not in devices:
        print("\n[!] Device not found.")
        return
    info = devices[device_id]
    print(f"\nCurrent: name={info['name']}  ip={info['ip']}  status={info['status']}  firmware={info['firmware']}")
    status = input("New status (ONLINE/OFFLINE/MAINTENANCE): ").strip()
    firmware = input("New firmware version: ").strip()
    update_configuration(device_id, status, firmware)      # no authentication (V3)
    print("\n[+] Configuration updated!")


def show_menu():
    print("\n==============================================")
    print("       IoT DEVICE MANAGEMENT SYSTEM")
    print("            GROUP 10  (vulnerable)")
    print("==============================================")
    print("1. Register Device\n2. List Devices\n3. Monitor Device Status\n4. Firmware Management")
    print("5. Update Configuration\n6. Exit")
    print("==============================================")


def main():
    setup_application()
    print("\nIoT Device Management System Started!")
    actions = {"1": register_device, "2": list_devices, "3": monitor_device,
               "4": firmware_management, "5": configuration_management}
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "6":
            print("\nThank you for using the system!\nExiting...")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("\n[!] Invalid choice.")


if __name__ == "__main__":
    main()
