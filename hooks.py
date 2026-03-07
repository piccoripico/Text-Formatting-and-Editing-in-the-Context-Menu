from __future__ import annotations

from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.reviewer import Reviewer

from .config_store import load_config
from .menu_builder import build_context_menu


def _on_editor_context_menu(editor, menu) -> None:
    config = load_config()
    if config["editor"]["enabled"]:
        build_context_menu(menu, "editor", editor.web)


def _on_reviewer_context_menu(reviewer, menu) -> None:
    config = load_config()
    if config["reviewer"]["enabled"]:
        build_context_menu(menu, "reviewer", reviewer.web)


def _on_webview_will_set_content(web_content, context) -> None:
    if not isinstance(context, (Editor, Reviewer)):
        return

    addon_package = mw.addonManager.addonFromModule(__name__)
    web_content.js.append(f"/_addons/{addon_package}/web/commands.js")


def register_hooks() -> None:
    gui_hooks.editor_will_show_context_menu.append(_on_editor_context_menu)
    gui_hooks.reviewer_will_show_context_menu.append(_on_reviewer_context_menu)
    gui_hooks.webview_will_set_content.append(_on_webview_will_set_content)