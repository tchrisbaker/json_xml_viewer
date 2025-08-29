import global_vars
from tree_utils import expand_all
from tree_utils import collapse_all
from tree_utils import insert_json
from tree_utils import insert_xml
import json
from tkinter import messagebox
import xml.etree.ElementTree as ET
from get_clipboard_text import get_clipboard_content
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
    tree_menu.add_command(label="Paste XML", command=lambda: paste_text("xml"))
    tree_menu.add_command(label="Paste JSON", command=lambda: paste_text("json"))
    global_vars.menu_bar.add_cascade(label="Tree", menu=tree_menu)

def paste_text(type):
    clipboard_content = get_clipboard_content()
    print("Clipboard contains:", clipboard_content)
    if (type == "json"):
        insert_json(global_vars.tree,'',clipboard_content)
    else:
        insert_xml(global_vars.tree, '', clipboard_content)

def paste_text(type):
    clipboard_content = get_clipboard_content()
    print("Clipboard contains:", clipboard_content)

    try:
        if type == "json":
            parsed = json.loads(clipboard_content)
            insert_json(global_vars.tree, '', parsed)
        elif type == "xml":
            root_element = ET.fromstring(clipboard_content)
            insert_xml(global_vars.tree, '', root_element)
        else:
            messagebox.showerror("Unsupported Format", "Only JSON and XML are supported.")
    except Exception as e:
        messagebox.showerror("Paste Error", f"Failed to parse clipboard content:\n{e}")

    