import os
import json
import hashlib
import time
import math
import psutil
from config import MONITORED_FOLDER, BASELINE_FILE, LOG_FILE



def calculate_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def scan_folder():
    file_hashes = {}
    for root, dirs, files in os.walk(MONITORED_FOLDER):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                file_hashes[full_path] = calculate_hash(full_path)
            except Exception:
                pass
    return file_hashes

def save_baseline(data):
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return {}
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)

def log_alert(message):
    # Ensure logs folder exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    # Write using UTF-8
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} - {message}\n")
    print("[ALERT]", message)

def create_baseline():
    print("Creating baseline...")
    data = scan_folder()
    save_baseline(data)
    print("Baseline created.")

ENTROPY_THRESHOLD = 7.5
PROCESS_THRESHOLD = 5
MONITORED_NAME = "dummy_process.py"

def detect_changes():
    print("Monitoring for changes...")
    baseline = load_baseline()

    if not baseline:
        print("No baseline found. Please create one first.")
        return

    while True:
        current_state = scan_folder()
        total_changes = 0
        changed_files = []

        # Detect new or modified files
        for file, hash_value in current_state.items():
            if file in baseline:
                if baseline[file] != hash_value:
                    total_changes += 1
                    changed_files.append(file)
            else:
                total_changes += 1
                changed_files.append(file)

        # Detect deleted files
        for file in baseline:
            if file not in current_state:
                total_changes += 1
                changed_files.append(file)
        
        detect_mass_process()

        # Only fire one alert per batch of changes
        if total_changes > 0:
            log_alert(f"⚠️ {total_changes} file(s) changed: {', '.join([os.path.basename(f) for f in changed_files])}")

            # High-entropy detection
            for file in changed_files:
                entropy = file_entropy(file)
                if entropy >= ENTROPY_THRESHOLD:
                    log_alert(f"⚠️ High entropy detected (possible encryption): {os.path.basename(file)} | Entropy: {entropy:.2f}")

            # Update baseline after alert to prevent repeated alerts
            baseline = current_state.copy()

        time.sleep(5)

def detect_mass_process():
    count = 0
    for proc in psutil.process_iter(attrs=['cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any(MONITORED_NAME in part for part in cmdline):
                count += 1
        except Exception:
            continue
    if count > PROCESS_THRESHOLD:
        log_alert(f"⚠️ Mass process detected: {count} '{MONITORED_NAME}' processes running!")
def file_entropy(filepath):
    """Calculate Shannon entropy of a file."""
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        if not data:
            return 0
        counts = [0] * 256
        for byte in data:
            counts[byte] += 1
        entropy = 0
        length = len(data)
        for count in counts:
            if count == 0:
                continue
            p = count / length
            entropy -= p * math.log2(p)
        return entropy
    except Exception:
        return 0
        
if __name__ == "__main__":
    print("1. Create baseline")
    print("2. Start monitoring")
    choice = input("Choose option: ")

    if choice == "1":
        create_baseline()
    elif choice == "2":
        detect_changes()