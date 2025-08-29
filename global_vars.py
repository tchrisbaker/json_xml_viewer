#globals
search_mode_var = None #search mode value in the search options
status_var = None # The status text at the bottom of the screen
case_var = None # case sensitivity value (true/false)
root = None # root window
recent_files = []  # Stores up to 5 recent file paths
search_entry = None # The search entry widget
tree = None # The treeview widget
recent_menu = None # The recent files menu object
menu_bar = None # The main menu bar
notebook = None  # The ttk.Notebook widget
trees = {}       # Dictionary to store Treeviews per tab
current_tab = None  # Currently active tab ID
update_recent_files_menu = None