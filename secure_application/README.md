# Secure Application - IoT Device Management System (Lab Assignment 3)

**Group 10** - application no. 10 (group number % 10 → IoT Device Management) | **Language:** Python 3 | **SAST tool:** Semgrep

A small console application that simulates IoT device management. It is **intentionally vulnerable** (exactly three vulnerabilities, as required) so that SAST findings can be studied; a hardened version shows the fixes.

## Core functionalities
1. Smart device registration
2. Device status monitoring (ping)
3. Firmware upload / view
4. Configuration management
5. Device listing

## Vulnerabilities demonstrated

| ID | Vulnerability | CWE | Location | Fix (hardened version) |
|----|---------------|-----|----------|------------------------|
| V1 | Command Injection | CWE-78 | `build_ping_command()`, `monitor_device_core()` (`shell=True`) | `ipaddress` validation, `subprocess.run([...], shell=False)` |
| V2 | Path Traversal | CWE-22 | `read_firmware()` | `realpath` + `commonpath` containment, extension allow-list |
| V3 | Missing Authentication | CWE-306 | `update_configuration()`, `upload_firmware()` | PBKDF2-HMAC-SHA256 login, session required |

## Folder structure
```
secure_application/
├── src/
│   ├── iot_device_manager.py          # vulnerable application (V1-V3)
│   ├── iot_device_manager_secure.py   # hardened application
│   ├── firmware_store/                # firmware files served by the app
│   └── internal/device_keys.txt       # FAKE secrets used to demonstrate V2
├── sast/
│   ├── run_scan.py                    # Semgrep runner
│   └── rules/iot_rules.yml            # custom rules, one per vulnerability
├── reports/                           # sast_report.txt / .json, Assignment_3_Report.pdf
├── screenshots/                       # app, exploits, Semgrep, tests
├── testcases/test_iot_manager.py      # 18 tests (functional + exploit proofs + fixes)
├── crypto/                            # reserved for later labs (cryptography is introduced later)
├── outputs/
└── README.md
```

## How to run
```bash
pip install semgrep                                   # SAST tool
python secure_application/src/iot_device_manager.py   # vulnerable app
python secure_application/src/iot_device_manager_secure.py   # hardened app (asks to create an admin password on first run)
python secure_application/sast/run_scan.py            # Semgrep with the lab rules (add --registry for the public rule-sets)
python secure_application/testcases/test_iot_manager.py -v   # 18 tests
```

## Proof-of-concept inputs
* **V1:** register a device with IP `127.0.0.1 & echo INJECTED_BY_ATTACKER`, then choose *Monitor Device Status*.
* **V2:** *Firmware Management → View* with filename `../internal/device_keys.txt`.
* **V3:** *Update Configuration* changes any device without any login.

## SAST result
Semgrep reports **5 findings, all in `iot_device_manager.py`** (V1 ×1, V2 ×2, V3 ×2) and none in the hardened file. See `reports/sast_report.txt`.
