"""
Lab Assignment 3
IoT Device Management System

Course  : Cryptography Laboratory (22CPP307)
Group   : 10
Language: Python
SAST    : Semgrep

Core Functionalities:
1. Device Registration
2. Device Status Monitoring
3. Firmware Management
4. Configuration Management
5. Device Listing

Intentional Vulnerabilities for SAST Detection:
1. Command Injection (subprocess with shell=True)
2. SQL Injection (Raw SQL query with string formatting)
3. Weak Hashing Algorithm (MD5 for password hashing)
4. Insecure File Handling / Path Traversal
"""

import os
import sys
import subprocess
import sqlite3
import hashlib


# ============================================================
#                    APPLICATION DATA & SECRETS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_FOLDER = os.path.join(BASE_DIR, "firmware_store")
DB_PATH = os.path.join(BASE_DIR, "iot_devices.db")
ADMIN_PASSWORD_HASH = hashlib.md5("admin123".encode()).hexdigest()  # VULNERABILITY: Weak Hashing (MD5)


devices = {
    "DEV101": {
        "name": "Smart Thermostat",
        "ip": "192.168.1.50",
        "status": "ONLINE",
        "firmware": "v1.0"
    },
    "DEV102": {
        "name": "Security Camera",
        "ip": "192.168.1.51",
        "status": "ONLINE",
        "firmware": "v2.0"
    },
    "DEV103": {
        "name": "Smart Door Lock",
        "ip": "192.168.1.52",
        "status": "OFFLINE",
        "firmware": "v1.2"
    }
}


# ============================================================
#                    SETUP FUNCTION
# ============================================================

def setup_application():
    os.makedirs(FIRMWARE_FOLDER, exist_ok=True)
    sample_file = os.path.join(FIRMWARE_FOLDER, "sample_firmware.txt")
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as file:
            file.write("Sample IoT Firmware\nVersion: 1.0\nDevice Type: Smart Device\n")

    # Setup SQLite database for SQL injection demo
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS devices (id TEXT, name TEXT, ip TEXT, status TEXT, firmware TEXT)")
    cursor.execute("DELETE FROM devices")
    cursor.execute("INSERT INTO devices VALUES ('DEV101', 'Smart Thermostat', '192.168.1.50', 'ONLINE', 'v1.0')")
    cursor.execute("INSERT INTO devices VALUES ('DEV102', 'Security Camera', '192.168.1.51', 'ONLINE', 'v2.0')")
    cursor.execute("INSERT INTO devices VALUES ('DEV103', 'Smart Door Lock', '192.168.1.52', 'OFFLINE', 'v1.2')")
    conn.commit()
    conn.close()



# ============================================================
#                 1. REGISTER DEVICE
# ============================================================

def register_device():
    print("\n================================")
    print("        REGISTER DEVICE")
    print("================================")

    device_id = input("Enter Device ID: ").strip()
    name = input("Enter Device Name: ").strip()
    ip = input("Enter IP Address: ").strip()

    if device_id == "" or name == "" or ip == "":
        print("\n[!] All fields are required.")
        return

    devices[device_id] = {
        "name": name,
        "ip": ip,
        "status": "REGISTERED",
        "firmware": "v1.0"
    }

    print("\n[+] Device registered successfully!")


# ============================================================
#                 2. VIEW DEVICES (SQL INJECTION DEMO)
# ============================================================

def view_devices():
    print("\n================================")
    print("         REGISTERED DEVICES")
    print("================================")

    search_id = input("Enter Device ID to search (leave blank for all): ").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if search_id:
        # --------------------------------------------------------
        # VULNERABILITY: SQL INJECTION (Raw string formatting in query)
        # --------------------------------------------------------
        query = f"SELECT * FROM devices WHERE id = '{search_id}'"
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for r in rows:
                print(f"\nID: {r[0]} | Name: {r[1]} | IP: {r[2]} | Status: {r[3]} | Firmware: {r[4]}")
        except Exception as e:
            print("\n[!] SQL Error:", e)
    else:
        cursor.execute("SELECT * FROM devices")
        rows = cursor.fetchall()
        for r in rows:
            print(f"\nID: {r[0]} | Name: {r[1]} | IP: {r[2]} | Status: {r[3]} | Firmware: {r[4]}")

    conn.close()


# ============================================================
#                 3. MONITOR DEVICE (COMMAND INJECTION)
# ============================================================

def monitor_device():
    print("\n================================")
    print("        DEVICE MONITORING")
    print("================================")

    device_id = input("Enter Device ID: ").strip()

    if device_id not in devices:
        print("\n[!] Device not found.")
        return

    ip = devices[device_id]["ip"]
    print("\nPinging device:", ip)

    # --------------------------------------------------------
    # VULNERABILITY: COMMAND INJECTION (shell=True with unsanitized string)
    # --------------------------------------------------------
    if os.name == "nt":
        command = "ping -n 1 " + ip
    else:
        command = "ping -c 1 " + ip

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        print("\n--- Ping Result ---")
        print(result.stdout[:500])
    except Exception as error:
        print("\n[!] Error:", error)


# ============================================================
#                 4. FIRMWARE MANAGEMENT (PATH TRAVERSAL)
# ============================================================

def firmware_management():
    while True:
        print("\n================================")
        print("       FIRMWARE MANAGEMENT")
        print("================================")
        print("1. View Firmware File")
        print("2. Upload Firmware")
        print("3. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_firmware()
        elif choice == "2":
            upload_firmware()
        elif choice == "3":
            break
        else:
            print("\n[!] Invalid choice.")


def view_firmware():
    print("\n--------------------------------")
    print("       VIEW FIRMWARE FILE")
    print("--------------------------------")

    filename = input("Enter firmware filename: ").strip()

    # --------------------------------------------------------
    # VULNERABILITY: INSECURE FILE HANDLING / PATH TRAVERSAL
    # --------------------------------------------------------
    file_path = os.path.join(FIRMWARE_FOLDER, filename)

    try:
        with open(file_path, "r") as file:
            print("\n--- File Contents ---")
            print(file.read())
            print("---------------------")
    except FileNotFoundError:
        print("\n[!] File not found.")
    except Exception as error:
        print("\n[!] Error:", error)


def upload_firmware():
    print("\n--------------------------------")
    print("        UPLOAD FIRMWARE")
    print("--------------------------------")

    device_id = input("Enter Device ID: ").strip()
    if device_id not in devices:
        print("\n[!] Device not found.")
        return

    source_file = input("Enter path of firmware file: ").strip()
    filename = input("Enter name for uploaded firmware: ").strip()

    destination = os.path.join(FIRMWARE_FOLDER, filename)

    try:
        with open(source_file, "rb") as source:
            data = source.read()
        with open(destination, "wb") as target:
            target.write(data)
        devices[device_id]["firmware"] = filename
        print("\n[+] Firmware uploaded successfully!")
    except FileNotFoundError:
        print("\n[!] Source file not found.")
    except Exception as error:
        print("\n[!] Error:", error)


# ============================================================
#                 5. UPDATE CONFIGURATION
# ============================================================

def update_configuration():
    print("\n================================")
    print("      UPDATE CONFIGURATION")
    print("================================")

    device_id = input("Enter Device ID: ").strip()
    if device_id not in devices:
        print("\n[!] Device not found.")
        return

    print("\nCurrent device information:")
    print("Name     :", devices[device_id]["name"])
    print("IP       :", devices[device_id]["ip"])
    print("Status   :", devices[device_id]["status"])
    print("Firmware :", devices[device_id]["firmware"])

    print("\nEnter new values.")
    new_status = input("Status (ONLINE/OFFLINE/MAINTENANCE): ").strip()
    new_firmware = input("Firmware version: ").strip()

    # --------------------------------------------------------
    # VULNERABILITY: WEAK AUTHENTICATION / PASSWORD HASH CHECK
    # --------------------------------------------------------
    entered_pass = input("Enter admin password to confirm update: ").strip()
    # Insecure MD5 Hash Comparison
    if hashlib.md5(entered_pass.encode()).hexdigest() != ADMIN_PASSWORD_HASH:
        print("\n[!] Admin authentication failed.")
        return

    if new_status != "":
        devices[device_id]["status"] = new_status
    if new_firmware != "":
        devices[device_id]["firmware"] = new_firmware

    print("\n[+] Configuration updated!")


# ============================================================
#                       MAIN MENU
# ============================================================

def show_menu():
    print("\n")
    print("==============================================")
    print("       IoT DEVICE MANAGEMENT SYSTEM")
    print("                 GROUP 10")
    print("==============================================")
    print("1. Register Device")
    print("2. View All Devices")
    print("3. Monitor Device Status")
    print("4. Firmware Management")
    print("5. Update Configuration")
    print("6. Exit")
    print("==============================================")


def main():
    setup_application()
    print("\nIoT Device Management System Started!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            register_device()
        elif choice == "2":
            view_devices()
        elif choice == "3":
            monitor_device()
        elif choice == "4":
            firmware_management()
        elif choice == "5":
            update_configuration()
        elif choice == "6":
            print("\nThank you for using the system!")
            print("Exiting...")
            break
        else:
            print("\n[!] Invalid choice.")


if __name__ == "__main__":
    main()