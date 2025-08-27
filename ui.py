from tkinterdnd2 import TkinterDnD,DND_FILES
import tkinter as tk
from tkinter import ttk

from open_file import open_file_dialog
from search import search_tree 

from tree_utils import expand_all
from tree_utils import collapse_all
import xml.etree.ElementTree as ET

import global_vars
from drag_drop import setupDnD
from recent_files import load_recent_files
from drag_drop import open_dropped_file
from context_menu import setup_context_menu
from shortcuts import setup_shortcuts
from tooltip import ToolTip
from tooltip import setup_tooltip
from searchbar import setup_search_bar
from searchbar import doSearch
from searchbar import doClearSearch
def render_json_tree():
    # Initialize main application window
    global_vars.root = TkinterDnD.Tk()
    global_vars.root.title("Tree Viewer")
    global_vars.root.geometry("800x600")

    # Tree widget with scrollbar
    tree_frame = tk.Frame(global_vars.root)
    tree_frame.pack(fill='both', expand=True)

    # add scrollbar to the tree
    tree_scrollbar = ttk.Scrollbar(tree_frame)
    tree_scrollbar.pack(side='right', fill='y')

    # the treeview
    global_vars.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set)
    tooltip = ToolTip(global_vars.tree)
    global_vars.tree.pack(side='left', fill='both', expand=True)

    tree_scrollbar.config(command=global_vars.tree.yview)

    #highlight
    style = ttk.Style()
    style.configure("Treeview.Highlighted", background="#ffd966")  # Light yellow

    global_vars.tree.tag_configure("highlight", background="#ffd966")

    # === status bar ==============================================================
    global_vars.status_var = tk.StringVar()
    status_bar = tk.Label(global_vars.root, textvariable=global_vars.status_var, anchor='w', relief='sunken')
    status_bar.pack(fill='x', side='bottom')

    # === Menu bar ================================================================
    menu_bar = tk.Menu(global_vars.root)

    def openFileDialog():
        #open_file_dialog(tree, global_vars.root, lambda path: add_to_recent_files(path, update_recent_files_menu))
        open_file_dialog(global_vars.tree, global_vars.root, update_recent_files_menu)
    def expandAll():
        expand_all(global_vars.tree)
    
    def collapseAll():
        collapse_all(global_vars.tree)

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
    setup_search_bar(tk, global_vars.tree, ttk)
   
    #recent files menu update function
    def update_recent_files_menu():
        recent_menu.delete(0, 'end')
        for path in global_vars.recent_files:
            recent_menu.add_command(label=path, command=lambda p=path: open_dropped_file(global_vars.tree, p, update_recent_files_menu))
    load_recent_files(update_recent_files_menu)
   
    #tooltip 
    setup_tooltip(global_vars.tree, tooltip)
    
    #Set up Drag and Drop
    setupDnD(global_vars.tree, update_recent_files_menu )
    
    # Bind right-click to tree
    # Context menu for tree items
    def search_selected(query):
        global_vars.search_entry.delete(0, tk.END)
        global_vars.search_entry.insert(0, query)
        search_tree(global_vars.tree, query)

    # setup context menu
    setup_context_menu(global_vars.tree, global_vars.root, search_selected)

    # Keyboard shortcuts
    setup_shortcuts(openFileDialog, doSearch, doClearSearch, expandAll, collapseAll)

    # add menu bar to the window
    global_vars.root.config(menu=menu_bar)
    global_vars.root.mainloop()
