import json
import tkinter as tk 
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
from recent_files import add_to_recent_files
def insert_xml(tree, parent, element):
    tag = element.tag
    node_text = f"{tag}"
    if element.attrib:
        node_text += f" {element.attrib}"
    node = tree.insert(parent, 'end', text=node_text)

    if element.text and element.text.strip():
        tree.insert(node, 'end', text=f"Text: {element.text.strip()}")

    for child in element:
        insert_xml(tree, node, child)

def insert_json(tree, parent, json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            node = tree.insert(parent, 'end', text=key)
            insert_json(tree, node, value)
    elif isinstance(json_data, list):
        for index, item in enumerate(json_data):
            node = tree.insert(parent, 'end', text=f"[{index}]")
            insert_json(tree, node, item)
    else:
        tree.insert(parent, 'end', text=str(json_data))

def open_file_dialog(tree, root, callback=None):
    file_path = filedialog.askopenfilename(
        title="Open JSON or XML File",
        filetypes=[("JSON and XML Files", "*.json *.xml"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            tree.delete(*tree.get_children())  # Clear previous tree
            file_name = file_path.split("/")[-1]  # or use os.path.basename(file_path)

            if file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                insert_json(tree, '', json_data)
            elif file_path.endswith('.xml'):
                import xml.etree.ElementTree as ET
                tree_data = ET.parse(file_path)
                root_element = tree_data.getroot()
                insert_xml(tree, '', root_element)
            else:
                messagebox.showerror("Unsupported Format", "Only .json and .xml files are supported.")
                return
            add_to_recent_files(file_path, callback)
            root.title(f"JSON/XML Tree Viewer - {file_name}")  # Update title bar
            #if callback:
                #callback(file_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")