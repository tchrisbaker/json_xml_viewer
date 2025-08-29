import global_vars
import json
from tkinter import messagebox
import xml.etree.ElementTree as ET
from utils import set_status
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from get_clipboard_text import get_clipboard_content
from tree_utils import insert_json, insert_xml, extract_tree, export_treeview_to_xml
import traceback

# === Tree Editing Features ===
def save_tree_as_xml():
    tree_widget = global_vars.tree
    if not tree_widget:
        messagebox.showerror("Error", "No active tree to save.")
        return

    try:
        xml_element = extract_tree(tree_widget, format='xml')
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            title="Save Tree as XML"
        )
        if file_path:
            export_treeview_to_xml(tree_widget, file_path)
            #tree_obj = ET.ElementTree(xml_element)
            #tree_obj.write(file_path, encoding='utf-8', xml_declaration=True)
            messagebox.showinfo("Success", f"Tree saved as XML to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save XML:\n{e}")
        traceback.print_exc()

def delete_nodes_by_name(tree, name):
    def recursive_delete(node):
        for child in tree.get_children(node):
            recursive_delete(child)
            if tree.item(child, 'text') == name:
                tree.delete(child)
    for root_node in tree.get_children():
        recursive_delete(root_node)

def rename_nodes_by_name(tree, old_name, new_name):
    def recursive_rename(node):
        if tree.item(node, 'text') == old_name:
            tree.item(node, text=new_name)
        for child in tree.get_children(node):
            recursive_rename(child)
    for root_node in tree.get_children():
        recursive_rename(root_node)

def save_tree_to_json(tree):
    data = extract_tree(tree, format='json')
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Saved", f"Tree saved to {file_path}")

def prompt_delete_nodes():
    name = simpledialog.askstring("Delete Nodes", "Enter node name to delete:")
    if name:
        delete_nodes_by_name(global_vars.tree, name)
        messagebox.showinfo("Deleted", f"Nodes named '{name}' deleted.")

def prompt_rename_nodes():
    old_name = simpledialog.askstring("Rename Nodes", "Enter current node name:")
    if old_name:
        new_name = simpledialog.askstring("Rename Nodes", f"Enter new name for '{old_name}':")
        if new_name:
            rename_nodes_by_name(global_vars.tree, old_name, new_name)
            messagebox.showinfo("Renamed", f"Nodes renamed from '{old_name}' to '{new_name}'.")

def setup_menu(tk, open_file_dialog, update_recent_files_menu, openFileDialog=None, expandAll=None, collapseAll=None):
    global_vars.menu_bar = tk.Menu(global_vars.root)

    # File menu
    file_menu = tk.Menu(global_vars.menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=lambda: openFileDialog(), accelerator="Ctrl+O")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=global_vars.root.quit, accelerator="Ctrl+Q")
    global_vars.menu_bar.add_cascade(label="File", menu=file_menu)
    
    #recent files
    global_vars.recent_menu = tk.Menu(file_menu, tearoff=0)
    file_menu.add_cascade(label="Recent Files", menu=global_vars.recent_menu)

    tree_menu = tk.Menu(global_vars.menu_bar, tearoff=0)
    tree_menu.add_command(label="Expand All", command=lambda: expandAll(), accelerator="Ctrl+E")
    tree_menu.add_command(label="Collapse All", command=lambda: collapseAll(), accelerator="Ctrl+Shift+E")
    tree_menu.add_command(label="Paste JSON/XML", command=lambda: paste_text_auto())
    tree_menu.add_command(label="Close Tab", command=close_current_tab)

    edit_menu = tk.Menu(global_vars.menu_bar, tearoff=0)
    edit_menu.add_command(label="Delete Nodes by Name", command=prompt_delete_nodes)
    edit_menu.add_command(label="Rename Nodes by Name", command=prompt_rename_nodes)
    edit_menu.add_command(label="Save Tree to JSON", command=lambda: save_tree_to_json(global_vars.tree))
    edit_menu.add_command(label="Save as XML", command=save_tree_as_xml)
    global_vars.menu_bar.add_cascade(label="Edit", menu=edit_menu)

    global_vars.menu_bar.add_cascade(label="Tree", menu=tree_menu)

def paste_text_auto():
    clipboard_content = get_clipboard_content()
    try:
        global_vars.tree.delete(*global_vars.tree.get_children())  # Clear previous tree
        parsed = json.loads(clipboard_content)
        insert_json(global_vars.tree, '', parsed)
        set_status("Pasted JSON from clipboard.")
    except json.JSONDecodeError:
        try:
            global_vars.tree.delete(*global_vars.tree.get_children())  # Clear previous tree
            root_element = ET.fromstring(clipboard_content)
            insert_xml(global_vars.tree, '', root_element)
            set_status("Pasted XML from clipboard.")
        except ET.ParseError:
            messagebox.showerror("Paste Error", "Clipboard does not contain valid JSON or XML.")
def close_current_tab():
    tab_id = global_vars.current_tab
    if tab_id:
        global_vars.notebook.forget(tab_id)
        del global_vars.trees[tab_id]

        # Update current tab reference
        tabs = global_vars.notebook.tabs()
        if tabs:
            new_tab = tabs[-1]
            global_vars.current_tab = new_tab
            global_vars.tree = global_vars.trees[new_tab]
        else:
            global_vars.current_tab = None
            global_vars.tree = None
