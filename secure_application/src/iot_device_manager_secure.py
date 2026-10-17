"""
Lab Assignment 3 - IoT Device Management System (HARDENED VERSION)

Same five functionalities as iot_device_manager.py, with the three
vulnerabilities remediated:

    V1  Command Injection      -> strict IP validation (ipaddress module) and
                                  subprocess.run([...], shell=False)
    V2  Path Traversal         -> resolved-path containment check + file-extension allow-list
    V3  Missing Authentication -> salted PBKDF2-HMAC-SHA256 login; privileged actions
                                  require an authenticated session (constant-time compare)
"""

import getpass
import hashlib
import hmac
import ipaddress
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_FOLDER = os.path.join(BASE_DIR, "firmware_store")
CREDENTIAL_FILE = os.path.join(BASE_DIR, "admin_credential.bin")   # created at first run, never committed
ALLOWED_EXTENSIONS = (".txt", ".bin", ".fw")
PBKDF2_ROUNDS = 200_000


def default_devices():
    return {
        "DEV101": {"name": "Smart Thermostat", "ip": "192.168.1.50", "status": "ONLINE",  "firmware": "v1.0"},
        "DEV102": {"name": "Security Camera",  "ip": "192.168.1.51", "status": "ONLINE",  "firmware": "v2.0"},
        "DEV103": {"name": "Smart Door Lock",  "ip": "192.168.1.52", "status": "OFFLINE", "firmware": "v1.2"},
    }


devices = default_devices()


# ---------------------------- authentication (fix V3) -----------------------
def hash_password(password, salt=None):
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ROUNDS)
    return salt + digest


def verify_password(password, stored):
    salt, digest = stored[:16], stored[16:]
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ROUNDS)
    return hmac.compare_digest(candidate, digest)


class Session:
    """Minimal authenticated-session object; privileged functions require one."""
    def __init__(self, user):
        self.user = user


def login(password, stored_credential):
    if verify_password(password, stored_credential):
        return Session("admin")
    return None


def require_auth(session):
    if not isinstance(session, Session):
        raise PermissionError("Authentication required")


# ---------------------------- input validation (fix V1) ---------------------
def validate_ip(ip):
    try:
        return str(ipaddress.ip_address(ip.strip()))
    except ValueError:
        raise ValueError("Invalid IP address")


def register_device_core(device_id, name, ip):
    if not device_id.isalnum() or len(device_id) > 20:
        raise ValueError("Device ID must be alphanumeric (max 20 chars)")
    if not name or len(name) > 40:
        raise ValueError("Device name required (max 40 chars)")
    devices[device_id] = {"name": name, "ip": validate_ip(ip), "status": "REGISTERED", "firmware": "v1.0"}


def build_ping_command(ip):
    flag = "-n" if os.name == "nt" else "-c"
    return ["ping", flag, "1", validate_ip(ip)]          # argument list: no shell involved


def monitor_device_core(device_id):
    command = build_ping_command(devices[device_id]["ip"])
    result = subprocess.run(command, shell=False, capture_output=True, text=True, timeout=10)
    return " ".join(command), result.stdout + result.stderr


# ---------------------------- safe file handling (fix V2) -------------------
def safe_firmware_path(filename, folder=FIRMWARE_FOLDER):
    base = os.path.realpath(folder)
    target = os.path.realpath(os.path.join(base, filename))
    if os.path.commonpath([base, target]) != base:
        raise PermissionError("Path traversal blocked")
    if not target.lower().endswith(ALLOWED_EXTENSIONS):
        raise PermissionError("File type not allowed")
    return target


def read_firmware(filename, folder=FIRMWARE_FOLDER):
    with open(safe_firmware_path(filename, folder), "r") as handle:
        return handle.read()


def upload_firmware(session, device_id, source_file, new_name, folder=FIRMWARE_FOLDER):
    require_auth(session)
    destination = safe_firmware_path(os.path.basename(new_name), folder)
    with open(source_file, "rb") as src:
        data = src.read()
    with open(destination, "wb") as dst:
        dst.write(data)
    devices[device_id]["firmware"] = os.path.basename(new_name)


def update_configuration(session, device_id, status=None, firmware=None):
    require_auth(session)
    if status:
        if status not in ("ONLINE", "OFFLINE", "MAINTENANCE"):
            raise ValueError("Invalid status")
        devices[device_id]["status"] = status
    if firmware:
        devices[device_id]["firmware"] = firmware[:40]


# ---------------------------- console UI -------------------------------------
def ensure_credential():
    if not os.path.exists(CREDENTIAL_FILE):
        print("First run: create an administrator password.")
        password = getpass.getpass("New password: ")
        with open(CREDENTIAL_FILE, "wb") as handle:
            handle.write(hash_password(password))
    with open(CREDENTIAL_FILE, "rb") as handle:
        return handle.read()


def main():
    os.makedirs(FIRMWARE_FOLDER, exist_ok=True)
    stored = ensure_credential()
    session = None
    while True:
        print("\n==============================================")
        print("   IoT DEVICE MANAGEMENT SYSTEM (hardened)")
        print("==============================================")
        print("1. Login\n2. List Devices\n3. Register Device\n4. Monitor Device\n5. View Firmware")
        print("6. Update Configuration (login required)\n7. Exit")
        choice = input("Enter your choice (1-7): ").strip()
        try:
            if choice == "1":
                session = login(getpass.getpass("Password: "), stored)
                print("[+] Logged in." if session else "[!] Login failed.")
            elif choice == "2":
                for dev_id, info in devices.items():
                    print(f"{dev_id} | {info['name']:<18} | {info['ip']:<15} | {info['status']}")
            elif choice == "3":
                register_device_core(input("ID: ").strip(), input("Name: ").strip(), input("IP: ").strip())
                print("[+] Registered.")
            elif choice == "4":
                command, output = monitor_device_core(input("Device ID: ").strip())
                print("Executing:", command, "\n", output[:300])
            elif choice == "5":
                print(read_firmware(input("Firmware file: ").strip()))
            elif choice == "6":
                update_configuration(session, input("Device ID: ").strip(),
                                     input("Status: ").strip(), input("Firmware: ").strip())
                print("[+] Updated.")
            elif choice == "7":
                break
            else:
                print("[!] Invalid choice.")
        except (ValueError, PermissionError, KeyError, OSError) as error:
            print("[!] Blocked:", error)


if __name__ == "__main__":
    main()
