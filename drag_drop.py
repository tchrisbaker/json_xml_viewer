import json
import xml.etree.ElementTree as ET
from tkinter import messagebox
from tkinterdnd2 import DND_FILES
from recent_files import add_to_recent_files
import global_vars
def open_dropped_file(tree, file_path, callback):
   
    # Clear existing tree content
    for item in tree.get_children():
        tree.delete(item)

    try:
        if file_path.lower().endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            from tree_utils import insert_json
            insert_json(tree, '', data)
            add_to_recent_files(file_path, callback)
        elif file_path.lower().endswith('.xml'):
            tree_obj = ET.parse(file_path)
            root_element = tree_obj.getroot()
            from tree_utils import insert_xml
            insert_xml(tree, '', root_element)
            add_to_recent_files(file_path, callback)
        else:
            messagebox.showerror("Unsupported File", "Only JSON and XML files are supported.")
        file_name = file_path.split("/")[-1]  # or use os.path.basename(file_path)
        global_vars.root.title(f"JSON/XML Tree Viewer - {file_name}")  # Update title bar
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file:\n{e}")

def setupDnD(tree, callback):
    
    def on_drop(event):
        file_path = event.data.strip('{}')  # Remove curly braces if present
        open_dropped_file(tree, file_path, callback)

    tree.drop_target_register(DND_FILES)
    tree.dnd_bind('<<Drop>>', on_drop)
