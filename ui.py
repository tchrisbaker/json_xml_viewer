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
from drag_drop import setupDnD
from recent_files import load_recent_files
from drag_drop import open_dropped_file
from context_menu import setup_context_menu
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
        #open_file_dialog(tree, global_vars.root, lambda path: add_to_recent_files(path, update_recent_files_menu))
        open_file_dialog(tree, global_vars.root, update_recent_files_menu)
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
    
    #recent files
    recent_menu = tk.Menu(file_menu, tearoff=0)
    file_menu.add_cascade(label="Recent Files", menu=recent_menu)

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
    def update_recent_files_menu():
        recent_menu.delete(0, 'end')
        for path in global_vars.recent_files:
            recent_menu.add_command(label=path, command=lambda p=path: open_dropped_file(tree, p, update_recent_files_menu))
    
    def doSearch(event=None):
        print("search")
        search_tree(tree, search_entry.get())

    def doClearSearch(event=None):
        #print("clear search")
        clear_search(tree, search_entry)
    load_recent_files(update_recent_files_menu)
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
        search_after_id = global_vars.root.after(2000, doSearch)

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
    
    #Set up Drag and Drop
    setupDnD(tree, update_recent_files_menu )
    
    # Bind right-click to tree
    # Context menu for tree items
    def search_selected(query):
        search_entry.delete(0, tk.END)
        search_entry.insert(0, query)
        search_tree(tree, query)
    setup_context_menu(tree, global_vars.root, search_selected)

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
