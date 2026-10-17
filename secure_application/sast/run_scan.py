"""
Semgrep SAST runner for the IoT Device Management application.

Scans src/ with (a) the lab's custom rules in sast/rules/iot_rules.yml and, when the
machine is online, (b) the public Semgrep registry rule-set (--config auto).
Reports are written to ../reports/ as text and JSON.

Usage:  python secure_application/sast/run_scan.py            (custom rules only)
        python secure_application/sast/run_scan.py --registry (custom + registry rules)
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")
RULES = os.path.join(HERE, "rules", "iot_rules.yml")
REPORTS = os.path.join(HERE, "..", "reports")


def run(extra_args, output_path):
    exe = shutil.which("semgrep")
    if exe is None:
        sys.exit("semgrep not found. Install it with:  pip install semgrep")
    cmd = [exe, "scan", "--metrics=off", "--no-git-ignore", "--disable-version-check", *extra_args]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=os.path.join(HERE, ".."))
    return result.stdout if result.stdout.strip() else result.stderr


def main():
    os.makedirs(REPORTS, exist_ok=True)
    configs = ["--config", RULES]
    if "--registry" in sys.argv:
        configs += ["--config", "auto"]
    target = "src"
    print(f"Running Semgrep on: {os.path.abspath(SRC)}\n")
    text = run([*configs, target], None)
    print(text)
    with open(os.path.join(REPORTS, "sast_report.txt"), "w", encoding="utf-8") as handle:
        handle.write(text)
    js = run([*configs, "--json", target], None)
    with open(os.path.join(REPORTS, "sast_report.json"), "w", encoding="utf-8") as handle:
        handle.write(js)
    print("Reports saved to", os.path.abspath(REPORTS))


if __name__ == "__main__":
    main()
