import global_vars

import json
import os

RECENT_FILE_PATH = "recent_files.json"

def load_recent_files(update_callback):
    print("loading recent files...")
    if os.path.exists(RECENT_FILE_PATH):
        print(f"{RECENT_FILE_PATH} found")
        try:
            with open(RECENT_FILE_PATH, "r") as f:
                data = json.load(f)
                
                global_vars.recent_files = data
                for d in global_vars.recent_files:
                    print (d)
                    add_to_recent_files(d, update_callback)
        except Exception as e:
            print(e)
            global_vars.recent_files = []
    else:
        global_vars.recent_files = []

def save_recent_files():
    try:
        with open(RECENT_FILE_PATH, "w") as f:
            json.dump(global_vars.recent_files, f)
    except Exception as e:
        print(f"Error saving recent files: {e}")

def add_to_recent_files(file_path, update_callback=None):
    if file_path in global_vars.recent_files:
        global_vars.recent_files.remove(file_path)
    global_vars.recent_files.insert(0, file_path)
    if len(global_vars.recent_files) > 5:
        global_vars.recent_files.pop()
    save_recent_files()
    if update_callback:
        update_callback()
