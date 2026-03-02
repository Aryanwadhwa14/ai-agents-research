import os
import json
import shutil

# Define source and target files
source_file = "results/session_recall.json"
target_file = "results/multi_session_rename.json"

# Check if source exists
if os.path.exists(source_file):
    shutil.copy(source_file, target_file)
    print(f"Renamed and saved: {target_file}")
else:
    print("session_recall.json not found. Run multi_session_recall.py first.")
