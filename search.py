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

#tooltip will show the full path
def get_full_path(node, tree):
    path_parts = []
    while node:
        text = tree.item(node, 'text')
        path_parts.insert(0, text)
        node = tree.parent(node)
    return " -> ".join(path_parts)

def cycle_match(tree, direction):
    global current_match_index
    if not search_matches:
        set_status("No matches to cycle through.")
        return

    current_match_index = (current_match_index + direction) % len(search_matches)
    node = search_matches[current_match_index]

    tree.selection_set(node)
    tree.focus(node)
    tree.see(node)

    path = get_full_path(node, tree)
    set_status(f"Focused match {current_match_index + 1} of {len(search_matches)}: {path}", clear_after=False)

