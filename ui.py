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
from menu import setup_menu
from tree_notebook import on_tab_change
from tree_notebook import create_new_tab
def render_json_tree():
    # Initialize main application window
    global_vars.root = TkinterDnD.Tk()
    global_vars.root.title("Tree Viewer")
    global_vars.root.geometry("800x600")

    #right-click menu for tab
    def show_tab_context_menu(event):
        #tab_id = global_vars.notebook.identify(event.x, event.y)
        tab_id = global_vars.notebook.index(f"@{event.x},{event.y}")
        tab_id = global_vars.notebook.tabs()[tab_id]
        if tab_id:
            global_vars.notebook.select(tab_id)
            global_vars.current_tab = tab_id
            global_vars.tree = global_vars.trees[tab_id]
            tab_menu.post(event.x_root, event.y_root)
    # close a tab
    def close_tab(tab_id):
        global_vars.notebook.forget(tab_id)
        if tab_id in global_vars.trees:
            del global_vars.trees[tab_id]

        tabs = global_vars.notebook.tabs()
        if tabs:
            new_tab = tabs[-1]
            global_vars.current_tab = new_tab
            global_vars.tree = global_vars.trees[new_tab]
        else:
            global_vars.current_tab = None
            global_vars.tree = None

    # Create notebook for tabs
    global_vars.notebook = ttk.Notebook(global_vars.root)
    global_vars.notebook.pack(fill='both', expand=True)
    global_vars.notebook.bind("<<NotebookTabChanged>>", on_tab_change)
    # allow user to close the tab via right-click
    tab_menu = tk.Menu(global_vars.root, tearoff=0)
    tab_menu.add_command(label="Close Tab", command=lambda: close_tab(global_vars.current_tab))
    global_vars.notebook.bind("<Button-3>", show_tab_context_menu)
   
    create_new_tab()

    # === status bar ==============================================================
    global_vars.status_var = tk.StringVar()
    status_bar = tk.Label(global_vars.root, textvariable=global_vars.status_var, anchor='w', relief='sunken')
    status_bar.pack(fill='x', side='bottom')

    # === Menu bar ================================================================
    # menu_bar = tk.Menu(global_vars.root)

    def openFileDialog():
        open_file_dialog(global_vars.tree, global_vars.root, update_recent_files_menu)
    def expandAll():
        expand_all(global_vars.tree)
    
    def collapseAll():
        collapse_all(global_vars.tree)

    # ==== Search bar ==========================================================
    setup_search_bar(tk, global_vars.tree, ttk)
   
    #recent files menu update function
    def update_recent_files_menu():
        global_vars.recent_menu.delete(0, 'end')
        for path in global_vars.recent_files:
            global_vars.recent_menu.add_command(label=path, command=lambda p=path: open_dropped_file(global_vars.tree, p, update_recent_files_menu))
    global_vars.update_recent_files_menu = update_recent_files_menu
    # set up the menu
    setup_menu(tk, open_file_dialog, update_recent_files_menu, openFileDialog, expandAll, collapseAll)

    # Load recent files at startup
    load_recent_files(update_recent_files_menu)
   
    #tooltip 
    #setup_tooltip(global_vars.tree, tooltip)
    
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
    global_vars.root.config(menu=global_vars.menu_bar)
    global_vars.root.mainloop()
