import global_vars
from search import search_tree 
from search import clear_search
from search import cycle_match
def setup_search_bar(tk, tree, ttk):
    # ==== Search bar ==========================================================
    #search results next and previous
    search_frame = tk.Frame(global_vars.root)
    search_frame.pack(fill='x', padx=5, pady=5)

    prev_button = tk.Button(search_frame, text="Previous", command=lambda: cycle_match(tree, -1))
    prev_button.pack(side='left', padx=5) 

    next_button = tk.Button(search_frame, text="Next", command=lambda: cycle_match(tree, 1))
    next_button.pack(side='left', padx=5)
    
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

    global_vars.search_entry = tk.Entry(search_frame)
    global_vars.search_entry.pack(side='left', fill='x', expand=True)
    
    search_after_id = None  # Global or closure variable to track scheduled search
    global_vars.search_entry.bind("<KeyRelease>")
    
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

    global_vars.search_entry.bind("<KeyRelease>", on_search_key)

def doSearch(event=None):
        print("search")
        search_tree(global_vars.tree, global_vars.search_entry.get())

def doClearSearch(event=None):
        #print("clear search")
        clear_search(global_vars.tree, global_vars.search_entry)