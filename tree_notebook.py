import global_vars
import tkinter as tk
from tkinter import ttk
from tooltip import ToolTip
from tooltip import setup_tooltip
from context_menu import setup_context_menu
from context_menu import search_selected
 
def create_new_tab(title="Untitled"):
    tab_frame = tk.Frame(global_vars.notebook)
    global_vars.notebook.add(tab_frame, text=title)
    global_vars.notebook.select(tab_frame)

    # Scrollbar
    scrollbar = ttk.Scrollbar(tab_frame)
    scrollbar.pack(side='right', fill='y')

    # Treeview
    tree = ttk.Treeview(tab_frame, yscrollcommand=scrollbar.set)
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=tree.yview)

    # Store tree
    tab_id = global_vars.notebook.tabs()[-1]
    global_vars.trees[tab_id] = tree
    global_vars.tree = tree  # Set current tree
    global_vars.current_tab = tab_id

    # Tooltip, context menu, etc.
    tooltip = ToolTip(tree)
    setup_tooltip(tree, tooltip)
    setup_context_menu(tree, global_vars.root, search_selected)
    #highlight
    style = ttk.Style()
    style.configure("Treeview.Highlighted", background="#ffd966")  # Light yellow
    tree.tag_configure("highlight", background="#ffd966")
    return tree 
def on_tab_change(event):
    selected_tab = global_vars.notebook.select()
    global_vars.tree = global_vars.trees[selected_tab]
    global_vars.current_tab = selected_tab

