import tkinter as tk
from tkinter import ttk
import global_vars;
from utils import set_status
# Global variable to store search matches and current index
search_matches = []
current_match_index = -1
search_after_id = None  # Global or closure variable to track scheduled search
def clear_highlights(tree):
    for item in tree.get_children():
        clear_node_highlight(tree, item)

def clear_node_highlight(tree, node):
    tree.item(node, tags=())
    for child in tree.get_children(node):
        clear_node_highlight(tree, child)
        
def search_tree(tree, query):
    clear_highlights(tree)  # Unhighlight previous matches
    match_count = 0
    
    case_sensitive = global_vars.case_var.get()
    
    search_mode = global_vars.search_mode_var.get()

    #for cyclying through matches
    global search_matches, current_match_index
    search_matches = []
    current_match_index = -1

    if not case_sensitive:
        query = query.lower()

    def search_node(node):
        nonlocal match_count
        text = tree.item(node, 'text')
        compare_text = text if case_sensitive else text.lower()

        match = False
        if search_mode == "Contains": # match using contains
            match = query in compare_text
        elif search_mode == "Starts With": #match using starts with
            match = compare_text.startswith(query)
        elif search_mode == "Ends With": #match using ends with
            match = compare_text.endswith(query)
        elif search_mode == "Exact Match": #match exactly
            match = compare_text == query

        if match and query: #if it is a match and query has text in it (query will be False if it is empty)
            tree.see(node) 
            tree.selection_add(node)
            tree.item(node, tags=("highlight",))
            search_matches.append(node)
            match_count += 1
        else:
            tree.selection_remove(node) #remove this node from the selection

        for child in tree.get_children(node): #iterate through the children of this node
            search_node(child)

    for item in tree.get_children(): #recursively search through the nodes and their children
        search_node(item) 

    set_status(f"{match_count} match{'es' if match_count != 1 else ''} found.", clear_after=False)


def clear_search(tree, search_entry):
    clear_highlights(tree)
    for item in tree.selection():
        tree.selection_remove(item)
    search_entry.delete(0, tk.END)
    set_status("Search cleared.")


""" def highlight_matches(tree):
    #Highlight all matched nodes.
    for node in tree.get_children():
        clear_highlight(tree, node)

    for node in search_matches:
        tree.item(node, tags=('match',))
    tree.tag_configure('match', background='yellow')

def clear_highlight(tree, node=''):
    #Clear all highlights recursively.
    tree.item(node, tags=())
    for child in tree.get_children(node):
        clear_highlight(tree, child) """

""" def clear_search(tree):
    #Clear search highlights and reset match index.
    global search_matches, current_match_index
    for node in tree.get_children():
        clear_highlight(tree, node)
    search_matches = []
    current_match_index = -1 """

def cycle_match(tree):
    """Cycle through matched nodes and focus on the current one."""
    global current_match_index
    if not search_matches:
        return
    current_match_index = (current_match_index + 1) % len(search_matches)
    node = search_matches[current_match_index]
    tree.see(node)
    tree.selection_set(node)
    tree.focus(node)

""" def setup_search_bar(root, tree):
    #Create a search bar UI and bind search functions
    frame = tk.Frame(root)
    frame.pack(fill=tk.X, padx=5, pady=5)

    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def on_search():
        query = entry.get()
        search_tree(tree, query)

    def on_clear():
        entry.delete(0, tk.END)
        clear_search(tree)

    def on_next():
        cycle_match(tree)

    tk.Button(frame, text="Search", command=on_search).pack(side=tk.LEFT, padx=2)
    tk.Button(frame, text="Clear", command=on_clear).pack(side=tk.LEFT, padx=2)
    tk.Button(frame, text="Next", command=on_next).pack(side=tk.LEFT, padx=2) """

""" 
def on_search_key(event, root, tree, search_entry):
    global search_after_id
    if search_after_id:
        root.after_cancel(search_after_id)
    search_after_id = root.after(300, lambda: search_tree(tree, search_entry.get())) """
