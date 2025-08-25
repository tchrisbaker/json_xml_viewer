import global_vars

def setup_shortcuts(openFileDialog, doSearch, doClearSearch, expandAll, collapseAll):
# Keyboard shortcuts
    global_vars.root.bind('<Control-o>', lambda e: openFileDialog())
    global_vars.root.bind('<Control-q>', lambda e: global_vars.root.quit())
    global_vars.root.bind('<Return>', doSearch)
    global_vars.root.bind('<Escape>', doClearSearch)
    global_vars.root.bind('<Control-e>', lambda e: expandAll())
    global_vars.root.bind('<Control-E>', lambda e: collapseAll())  # Shift+Ctrl+E 