# attacker/ransomware_sim.py
import os
import time

TARGET_FOLDER = "../monitored_folder"

def simulate_ransomware():
    files = [f for f in os.listdir(TARGET_FOLDER) if os.path.isfile(os.path.join(TARGET_FOLDER, f))]
    
    print(f"Simulating ransomware on {len(files)} file(s)...")
    
    # 1️⃣ Modify existing files
    for filename in files:
        filepath = os.path.join(TARGET_FOLDER, filename)
        size = os.path.getsize(filepath)
        with open(filepath, "r+b") as f:
            f.seek(0)
            f.write(os.urandom(size))  # random bytes = high entropy
        print(f"Modified (simulated encryption) {filename}")
        time.sleep(0.3)
    
    # 2️⃣ Create new files
    for i in range(2):
        new_file = os.path.join(TARGET_FOLDER, f"new_file_{i+1}.txt")
        with open(new_file, "wb") as f:
            f.write(os.urandom(512))  # random content
        print(f"Created new file {new_file}")
        time.sleep(0.3)
    
    # 3️⃣ Delete a file (if any left)
    if files:
        file_to_delete = os.path.join(TARGET_FOLDER, files[0])
        os.remove(file_to_delete)
        print(f"Deleted file {file_to_delete}")

if __name__ == "__main__":
    simulate_ransomware()