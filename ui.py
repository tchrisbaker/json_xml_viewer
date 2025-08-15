from tkinterdnd2 import TkinterDnD,DND_FILES
import tkinter as tk
from tkinter import ttk, messagebox

from open_file import open_file_dialog
from search import search_tree 
from search import clear_search
from search import get_full_path
from search import cycle_match
from utils import set_status
from tree_utils import expand_all
from tree_utils import collapse_all
import xml.etree.ElementTree as ET
import json
import global_vars

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, text, x, y):
        self.hide_tip()
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
            
def render_json_tree():
    global_vars.root = TkinterDnD.Tk()
    global_vars.root.title("Tree Viewer")
    global_vars.root.geometry("800x600")


    # Tree widget with scrollbar
    tree_frame = tk.Frame(global_vars.root)
    tree_frame.pack(fill='both', expand=True)

    tree_scrollbar = ttk.Scrollbar(tree_frame)
    tree_scrollbar.pack(side='right', fill='y')

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set)
    tooltip = ToolTip(tree)
    tree.pack(side='left', fill='both', expand=True)

    tree_scrollbar.config(command=tree.yview)

    #highlight
    style = ttk.Style()
    style.configure("Treeview.Highlighted", background="#ffd966")  # Light yellow

    tree.tag_configure("highlight", background="#ffd966")

    # === status bar ==============================================================
    global_vars.status_var = tk.StringVar()
    status_bar = tk.Label(global_vars.root, textvariable=global_vars.status_var, anchor='w', relief='sunken')
    status_bar.pack(fill='x', side='bottom')

    # === Menu bar ================================================================
    menu_bar = tk.Menu(global_vars.root)
    
    def openFileDialog(): 
        open_file_dialog(tree, global_vars.root)

    def expandAll():
        expand_all(tree)
    
    def collapseAll():
        collapse_all(tree)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=lambda: openFileDialog(), accelerator="Ctrl+O")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=global_vars.root.quit, accelerator="Ctrl+Q")
    menu_bar.add_cascade(label="File", menu=file_menu)

    tree_menu = tk.Menu(menu_bar, tearoff=0)
    tree_menu.add_command(label="Expand All", command=lambda: expandAll(), accelerator="Ctrl+E")
    tree_menu.add_command(label="Collapse All", command=lambda: collapseAll(), accelerator="Ctrl+Shift+E")
    menu_bar.add_cascade(label="Tree", menu=tree_menu)

    # ==== Search bar ==========================================================
    #search results next and previous
    search_frame = tk.Frame(global_vars.root)
    search_frame.pack(fill='x', padx=5, pady=5)

    next_button = tk.Button(search_frame, text="Next", command=lambda: cycle_match(tree, 1))
    next_button.pack(side='left', padx=5)

    prev_button = tk.Button(search_frame, text="Previous", command=lambda: cycle_match(tree, -1))
    prev_button.pack(side='left', padx=5) 
    
    global_vars.case_var = tk.BooleanVar()

    case_check = tk.Checkbutton(search_frame, text="Case Sensitive", variable=global_vars.case_var)
    case_check.pack(side='left', padx=5)
    
    global_vars.case_var.trace_add("write", lambda *args: doSearch())

    search_modes = ["Contains", "Starts With", "Ends With", "Exact Match"]
    global_vars.search_mode_var = tk.StringVar(value=search_modes[0])

    search_mode_menu = ttk.Combobox(search_frame, textvariable=global_vars.search_mode_var, values=search_modes, state="readonly", width=12)
    search_mode_menu.pack(side='left', padx=5)

    search_label = tk.Label(search_frame, text="Search:")
    search_label.pack(side='left')

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side='left', fill='x', expand=True)
    search_after_id = None  # Global or closure variable to track scheduled search
    search_entry.bind("<KeyRelease>")

    def doSearch(event=None):
        print("search")
        search_tree(tree, search_entry.get())

    def doClearSearch(event=None):
        #print("clear search")
        clear_search(tree, search_entry)

    search_button = tk.Button(search_frame, text="Search", command=doSearch)
    search_button.pack(side='left', padx=5)

    clear_button = tk.Button(search_frame, text="Clear", command=doClearSearch)
    clear_button.pack(side='left', padx=5) 

    #bind ui elements
     # Bind the event
    search_mode_menu.bind("<<ComboboxSelected>>", doSearch)
    case_check.bind("<<CheckBoxSelected>>", doSearch)

    #search each time the user presses a key in the search bar
    def on_search_key(event):
        nonlocal search_after_id
        if search_after_id:
            global_vars.root.after_cancel(search_after_id)
        search_after_id = global_vars.root.after(300, doSearch)

    search_entry.bind("<KeyRelease>", on_search_key)

    #tooltip 
    def on_motion(event):
        node = tree.identify_row(event.y)
        if node:
            full_path = get_full_path(node, tree)
            tooltip.show_tip(full_path, event.x_root + 10, event.y_root + 10)
        else:
            tooltip.hide_tip()

    def on_leave(event):
        tooltip.hide_tip()

    tree.bind("<Motion>", on_motion)
    tree.bind("<Leave>", on_leave)
    
    #handle drag & drop
    def handle_drop(event):
        file_path = event.data.strip('{}')  # Remove curly braces if present
        if file_path.endswith('.json') or file_path.endswith('.xml'):
            open_dropped_file(tree, global_vars.root, file_path)
        else:
            messagebox.showerror("Unsupported Format", "Only .json and .xml files are supported.")

    tree.drop_target_register(DND_FILES)
    tree.dnd_bind('<<Drop>>', handle_drop)

    def open_dropped_file(tree, root, file_path):
        try:
            tree.delete(*tree.get_children())
            file_name = file_path.split("/")[-1]
            if file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                insert_json(tree, '', json_data)
            elif file_path.endswith('.xml'):
                import xml.etree.ElementTree as ET
                tree_data = ET.parse(file_path)
                root_element = tree_data.getroot()
                insert_xml(tree, '', root_element)
            global_vars.root.title(f"JSON/XML Tree Viewer - {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

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

    # Bind right-click to tree
    # Context menu for tree items
    context_menu = tk.Menu(global_vars.root, tearoff=0)
    context_menu.add_command(label="Copy", command=lambda: copy_selected(tree))
    context_menu.add_command(label="Copy Full Path", command=lambda: copy_full_path(tree))
    context_menu.add_command(label="Expand", command=lambda: expand_selected(tree))
    context_menu.add_command(label="Search", command=lambda: search_selected(tree))

    def copy_full_path(tree):
        selected = tree.selection()
        if selected:
            node = selected[0]
            path_parts = []
            while node:
                text = tree.item(node, 'text')
                path_parts.insert(0, text)
                node = tree.parent(node)
            full_path = ".".join(path_parts)
            global_vars.root.clipboard_clear()
            global_vars.root.clipboard_append(full_path)
            global_vars.root.update()
            # Update status bar
            current_status = global_vars.status_var.get()
            set_status(f"Copied full path '{full_path}'. {current_status}")

    def copy_selected(tree):
        selected = tree.selection()
        if selected:
            value = tree.item(selected[0], 'text')
            global_vars.root.clipboard_clear()
            global_vars.root.clipboard_append(value)
            global_vars.root.update()  # Keeps clipboard content after app closes
            # Update status bar with copy confirmation
            current_status = global_vars.status_var.get()
            set_status(f"Copied '{value}'. {current_status}")

    
    def search_selected(tree):
        selected = tree.selection()
        if selected:
            value = tree.item(selected[0], 'text')
            search_entry.delete(0, tk.END)
            search_entry.insert(0, value)
            search_tree(tree, value)

    def expand_selected(tree):
        selected = tree.selection()
        if selected:
            def expand_node(node):
                tree.item(node, open=True)
                for child in tree.get_children(node):
                    expand_node(child)
            expand_node(selected[0])

    def show_context_menu(event):
        item_id = tree.identify_row(event.y)
        if item_id:
            tree.selection_set(item_id)
            context_menu.post(event.x_root, event.y_root)
    tree.bind("<Button-3>", show_context_menu)

    # Keyboard shortcuts
    global_vars.root.bind('<Control-o>', lambda e: openFileDialog())
    global_vars.root.bind('<Control-q>', lambda e: global_vars.root.quit())
    global_vars.root.bind('<Return>', doSearch)
    global_vars.root.bind('<Escape>', doClearSearch)
    global_vars.root.bind('<Control-e>', lambda e: expandAll())
    global_vars.root.bind('<Control-E>', lambda e: collapseAll())  # Shift+Ctrl+E 

    # add menu bar to the window
    global_vars.root.config(menu=menu_bar)
    global_vars.root.mainloop()
