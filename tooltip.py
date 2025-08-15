import tkinter as tk

class ToolTip:
    """Class to create a tooltip for a given widget."""
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, text, x, y):
        """Display the tooltip with the given text at (x, y)."""
        self.hide_tip()
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        """Hide the tooltip if it is visible."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def get_full_path(tree, node):
    """Get the full path of a node in the Treeview."""
    path = []
    while node:
        path.insert(0, tree.item(node, 'text'))
        node = tree.parent(node)
    return "/".join(path)

def setup_tooltip(tree, tooltip):
    """Bind mouse events to show full path tooltips on hover."""
    def on_motion(event):
        node = tree.identify_row(event.y)
        if node:
            full_path = get_full_path(tree, node)
            tooltip.show_tip(full_path, event.x_root + 10, event.y_root + 10)
        else:
            tooltip.hide_tip()

    def on_leave(event):
        tooltip.hide_tip()

    tree.bind("<Motion>", on_motion)
    tree.bind("<Leave>", on_leave)
