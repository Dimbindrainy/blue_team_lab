# attacker/mass_process_attack.py
import subprocess
import os
import time

DUMMY_PROCESS = "dummy_process.py"
NUM_PROCESSES = 10   # number of processes to spawn
DELAY_BETWEEN = 0.2  # seconds between each spawn

def mass_spawn():
    script_path = os.path.join(os.path.dirname(__file__), DUMMY_PROCESS)
    print(f"Spawning {NUM_PROCESSES} dummy processes...")

    for i in range(NUM_PROCESSES):
        subprocess.Popen(["python", script_path])
        print(f"Spawned process {i+1}")
        time.sleep(DELAY_BETWEEN)

if __name__ == "__main__":
    mass_spawn()