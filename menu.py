import global_vars
from tree_utils import expand_all
from tree_utils import collapse_all
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
    global_vars.menu_bar.add_cascade(label="Tree", menu=tree_menu)