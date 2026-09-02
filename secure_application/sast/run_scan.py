# Semgrep SAST scan runner script
import os
import sys
import subprocess

# Ensure UTF-8 output encoding for Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_sast_scan():
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    report_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "sast_report.txt"))
    json_report = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "sast_report.json"))

    print(f"Running Semgrep scan on: {src_dir}\n")
    cmd = f"semgrep scan --config auto \"{src_dir}\""
    
    env = os.environ.copy()
    env["PATH"] = r"C:\Users\saini\AppData\Roaming\Python\Python313\Scripts;" + env.get("PATH", "")
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore", env=env)
    
    output_text = result.stdout if result.stdout else result.stderr
    
    # Safely print to terminal
    try:
        print(output_text)
    except Exception:
        print(output_text.encode('ascii', 'ignore').decode('ascii'))

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(output_text)
        
    print(f"\nText report saved to: {report_file}")

    # Generate JSON report as well
    json_cmd = f"semgrep scan --config auto --json \"{src_dir}\""
    json_result = subprocess.run(json_cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore", env=env)
    with open(json_report, "w", encoding="utf-8") as f:
        f.write(json_result.stdout)
    print(f"JSON report saved to: {json_report}")

if __name__ == "__main__":
    run_sast_scan()
