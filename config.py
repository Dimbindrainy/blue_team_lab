import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MONITORED_FOLDER = os.path.join(BASE_DIR, "monitored_folder")
BASELINE_FILE = os.path.join(BASE_DIR, "baseline.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "alerts.log")