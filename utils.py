import global_vars
#method for setting the status on the status bar
def set_status(message, clear_after=True, duration=3000):
    global_vars.status_var.set(message)
    if clear_after:
        global_vars.root.after(duration, lambda: global_vars.status_var.set(""))