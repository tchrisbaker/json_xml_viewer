import pyperclip

def get_clipboard_content():
    # Get text from the clipboard
    clipboard_content = pyperclip.paste()

    return clipboard_content
