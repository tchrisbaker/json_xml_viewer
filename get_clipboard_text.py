import pyperclip

def get_clipboard_content():
    # Get text from the clipboard
    clipboard_content = pyperclip.paste()

    print("Clipboard contains:", clipboard_content)
    return clipboard_content
