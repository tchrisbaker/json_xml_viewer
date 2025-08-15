from tkinterdnd2 import TkinterDnD
import tkinter as tk
from tkinter import ttk
from open_file import open_file_dialog
from search import search_tree 
from search import clear_search
from tree_utils import expand_all
from tree_utils import collapse_all
import global_vars

def render_json_tree():
    global_vars.root = TkinterDnD.Tk()
    global_vars.root.title("Tree Viewer")
    global_vars.root.geometry("800x600")


    # Placeholder for setting up other components
    # setup_search_bar(root, tree)
    # setup_context_menu(root, tree)
    # setup_drag_and_drop(tree, root)
    # tooltip = ToolTip(tree)
    # setup_tooltip(tree, tooltip)

    # Tree widget with scrollbar
    tree_frame = tk.Frame(global_vars.root)
    tree_frame.pack(fill='both', expand=True)

    tree_scrollbar = ttk.Scrollbar(tree_frame)
    tree_scrollbar.pack(side='right', fill='y')

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set)
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

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=lambda: open_file_dialog(tree, global_vars.root), accelerator="Ctrl+O")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=global_vars.root.quit, accelerator="Ctrl+Q")
    menu_bar.add_cascade(label="File", menu=file_menu)

    tree_menu = tk.Menu(menu_bar, tearoff=0)
    tree_menu.add_command(label="Expand All", command=lambda: expand_all(tree), accelerator="Ctrl+E")
    tree_menu.add_command(label="Collapse All", command=lambda: collapse_all(tree), accelerator="Ctrl+Shift+E")
    menu_bar.add_cascade(label="Tree", menu=tree_menu)

    # ==== Search bar ==========================================================
    #search results next and previous
    search_frame = tk.Frame(global_vars.root)
    search_frame.pack(fill='x', padx=5, pady=5)

    """ next_button = tk.Button(search_frame, text="Next", command=lambda: cycle_match(tree, 1))
    next_button.pack(side='left', padx=5)

    prev_button = tk.Button(search_frame, text="Previous", command=lambda: cycle_match(tree, -1))
    prev_button.pack(side='left', padx=5)  """
    
    global_vars.case_var = tk.BooleanVar()

    case_check = tk.Checkbutton(search_frame, text="Case Sensitive", variable=global_vars.case_var)
    case_check.pack(side='left', padx=5)

    #whole_word_check = tk.Checkbutton(search_frame, text="Whole Word", variable=whole_word_var)
    #whole_word_check.pack(side='left', padx=5)

    search_modes = ["Contains", "Starts With", "Ends With", "Exact Match"]
    global_vars.search_mode_var = tk.StringVar(value=search_modes[0])

    search_mode_menu = ttk.Combobox(search_frame, textvariable=global_vars.search_mode_var, values=search_modes, state="readonly", width=12)
    search_mode_menu.pack(side='left', padx=5)


    search_label = tk.Label(search_frame, text="Search:")
    search_label.pack(side='left')

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side='left', fill='x', expand=True)
    #search_after_id = None  # Global or closure variable to track scheduled search
    search_entry.bind("<KeyRelease>")

    search_button = tk.Button(search_frame, text="Search", command=lambda: search_tree(tree, search_entry.get()))
    search_button.pack(side='left', padx=5)

    clear_button = tk.Button(search_frame, text="Clear", command=lambda: clear_search(tree, search_entry))
    clear_button.pack(side='left', padx=5) 

    #shortcuts
    # Keyboard shortcuts
    global_vars.root.bind('<Control-o>', lambda e: open_file_dialog(tree, global_vars.root))
    global_vars.root.bind('<Control-q>', lambda e: global_vars.root.quit())
    global_vars.root.bind('<Return>', lambda e: search_tree(tree, search_entry.get()))
    global_vars.root.bind('<Escape>', lambda e: clear_search(tree, search_entry))
    global_vars.root.bind('<Control-e>', lambda e: expand_all(tree))
    global_vars.root.bind('<Control-E>', lambda e: collapse_all(tree))  # Shift+Ctrl+E 

    # add menu bar to the window
    global_vars.root.config(menu=menu_bar)
    global_vars.root.mainloop()
