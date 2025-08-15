import json
import xml.etree.ElementTree as ET
from tkinter import messagebox
from tkinterdnd2 import DND_FILES

def open_dropped_file(tree, root, file_path):
    """Open and parse a dropped JSON or XML file into the Treeview."""
    # Clear existing tree content
    for item in tree.get_children():
        tree.delete(item)

    try:
        if file_path.lower().endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            from tree_utils import insert_json
            insert_json(tree, '', data)

        elif file_path.lower().endswith('.xml'):
            tree_obj = ET.parse(file_path)
            root_element = tree_obj.getroot()
            from tree_utils import insert_xml
            insert_xml(tree, '', root_element)

        else:
            messagebox.showerror("Unsupported File", "Only JSON and XML files are supported.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file:\n{e}")

def setup_drag_and_drop(tree, root):
    """Enable drag-and-drop file loading for the Treeview."""
    def on_drop(event):
        file_path = event.data.strip('{}')  # Remove curly braces if present
        open_dropped_file(tree, root, file_path)

    tree.drop_target_register(DND_FILES)
    tree.dnd_bind('<<Drop>>', on_drop)
