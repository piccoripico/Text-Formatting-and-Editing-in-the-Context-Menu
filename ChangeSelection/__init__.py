from aqt import gui_hooks, mw
from aqt.qt import QAction
from aqt.editor import EditorWebView
from aqt.reviewer import Reviewer

def exec_command(web_instance, command, value=None):
    if value:
        cmd = f"document.execCommand('{command}', false, '{value}');"
    else:
        cmd = f"document.execCommand('{command}', false, null);"
    web_instance.eval(cmd)

def build_selection_menu(web_instance, menu):
    selection_menu = menu.addMenu("Change Selection")

    actions = [
        ("Make Red", "foreColor", "red"),
        ("Make Subscript", "subscript", None),
        ("Make Strikethrough", "strikeThrough", None),
        ("Make Bold", "bold", None),
        ("Make Italic", "italic", None),
        ("Make Underlined", "underline", None),
        ("Reset", "removeFormat", None),
    ]

    for action_name, command, value in actions:
        action = QAction(action_name, menu)
        action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
        selection_menu.addAction(action)

def on_editor_context_menu(webview: EditorWebView, menu):
    web_instance = webview.editor.web
    build_selection_menu(web_instance, menu)

def on_reviewer_context_menu(webview, menu):
    reviewer = webview.parent().parent()
    web_instance = reviewer.web
    build_selection_menu(web_instance, menu)

gui_hooks.editor_will_show_context_menu.append(on_editor_context_menu)
gui_hooks.webview_will_show_context_menu.append(on_reviewer_context_menu)
