import global_vars
from tree_utils import expand_all
from tree_utils import collapse_all
from tree_utils import insert_json
from tree_utils import insert_xml
import json
from tkinter import messagebox
import xml.etree.ElementTree as ET
from utils import set_status
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
    tree_menu.add_command(label="Paste JSON/XML", command=lambda: paste_text_auto())
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
