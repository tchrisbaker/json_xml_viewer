import tkinter as tk
from tkinter import Menu
from tkinter import messagebox

def copy_selected(tree, root):
    """Copy the selected item's text to clipboard."""
    selected = tree.selection()
    if selected:
        text = tree.item(selected[0], 'text')
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
    else:
        messagebox.showinfo("Copy Selected", "No item selected.")

def copy_full_path(tree, root):
    """Copy the full path of the selected item to clipboard."""
    selected = tree.selection()
    if selected:
        path = []
        node = selected[0]
        while node:
            path.insert(0, tree.item(node, 'text'))
            node = tree.parent(node)
        full_path = "/".join(path)
        root.clipboard_clear()
        root.clipboard_append(full_path)
        root.update()
    else:
        messagebox.showinfo("Copy Full Path", "No item selected.")

def expand_selected(tree):
    """Expand the selected node and all its children."""
    selected = tree.selection()
    if selected:
        def expand(node):
            tree.item(node, open=True)
            for child in tree.get_children(node):
                expand(child)
        expand(selected[0])
    else:
        messagebox.showinfo("Expand Selected", "No item selected.")

def search_selected(tree, search_callback):
    """Search using the selected item's text."""
    selected = tree.selection()
    if selected:
        query = tree.item(selected[0], 'text')
        search_callback(query)
    else:
        messagebox.showinfo("Search Selected", "No item selected.")

def setup_context_menu(tree, root, search_callback=None):
    """Set up right-click context menu for the Treeview."""
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Copy Selected", command=lambda: copy_selected(tree, root))
    menu.add_command(label="Copy Full Path", command=lambda: copy_full_path(tree, root))
    menu.add_command(label="Expand Selected", command=lambda: expand_selected(tree))
    if search_callback:
        menu.add_command(label="Search Selected", command=lambda: search_selected(tree, search_callback))

    def show_context_menu(event):
        selected = tree.identify_row(event.y)
        if selected:
            tree.selection_set(selected)
            menu.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_context_menu)
