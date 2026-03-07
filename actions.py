from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from aqt.qt import QApplication, QFontDialog, QInputDialog
from aqt.utils import showInfo
from aqt.webview import AnkiWebView

from .menu_spec import CommandSpec


def _run_js(
    web: AnkiWebView,
    payload: dict[str, Any],
    callback: Callable[[Any], None] | None = None,
) -> None:
    js = f"window.CMTT && window.CMTT.exec({json.dumps(payload, ensure_ascii=False)});"
    if callback:
        web.page().runJavaScript(js, callback)
    else:
        web.eval(js)


def _insert_text(web: AnkiWebView, text: str) -> None:
    _run_js(web, {"op": "insertText", "text": text})


def _insert_html(web: AnkiWebView, html: str) -> None:
    _run_js(web, {"op": "insertHTML", "html": html})


def _normalize_image_source(src: str) -> str:
    src = src.strip()
    if not src:
        return src

    parsed = urlparse(src)
    if parsed.scheme:
        return src

    path = Path(src).expanduser()
    if path.exists():
        try:
            return path.resolve().as_uri()
        except Exception:
            return src

    return src


def _paste_from_clipboard(web: AnkiWebView) -> None:
    clipboard = QApplication.clipboard()
    mime = clipboard.mimeData()

    if mime is not None and mime.hasHtml():
        html = mime.html() or ""
        if html:
            _insert_html(web, html)
            return

    _insert_text(web, clipboard.text() or "")


def dispatch_spec(web: AnkiWebView, spec: CommandSpec) -> None:
    action = spec.action

    if action == "insert_text":
        _insert_text(web, str(spec.arg))
        return

    if action == "insert_html":
        _insert_html(web, str(spec.arg))
        return

    if action == "insert_datetime":
        text = datetime.now().strftime(str(spec.arg))
        _insert_text(web, text)
        return

    if action == "font_dialog":
        font, ok = QFontDialog.getFont()
        if ok:
            style: dict[str, str] = {"fontFamily": font.family()}
            if font.pointSize() > 0:
                style["fontSize"] = f"{font.pointSize()}pt"
            if font.bold():
                style["fontWeight"] = "bold"
            if font.italic():
                style["fontStyle"] = "italic"

            decorations: list[str] = []
            if font.underline():
                decorations.append("underline")
            if font.strikeOut():
                decorations.append("line-through")
            if decorations:
                style["textDecoration"] = " ".join(decorations)

            _run_js(web, {"op": "applyStyle", "style": style})
        return

    if action == "insert_link_prompt":
        url, ok = QInputDialog.getText(None, "Insert Link", "URL:")
        if ok and url.strip():
            _run_js(web, {"op": "insertLink", "url": url.strip()})
        return

    if action == "insert_image_prompt":
        url, ok = QInputDialog.getText(None, "Insert Image", "Image URL or path:")
        if ok and url.strip():
            _run_js(web, {"op": "insertImage", "url": _normalize_image_source(url)})
        return

    if action == "word_count":
        _run_js(
            web,
            {"op": "wordCount"},
            lambda result: showInfo(
                f"Words: {(result or {}).get('words', 0)}\n"
                f"Characters: {(result or {}).get('characters', 0)}"
            ),
        )
        return

    if action == "copy":
        _run_js(
            web,
            {"op": "getSelectedText"},
            lambda result: QApplication.clipboard().setText(result or ""),
        )
        return

    if action == "cut":
        def after_copy(result: Any) -> None:
            QApplication.clipboard().setText(result or "")
            _run_js(web, {"op": "deleteSelection"})

        _run_js(web, {"op": "getSelectedText"}, after_copy)
        return

    if action == "paste":
        _paste_from_clipboard(web)
        return

    if action == "paste_plain_text":
        _insert_text(web, QApplication.clipboard().text() or "")
        return

    if action == "undo":
        _run_js(web, {"op": "compatCommand", "command": "undo"})
        return

    if action == "redo":
        _run_js(web, {"op": "compatCommand", "command": "redo"})
        return

    if action == "remove_link":
        _run_js(web, {"op": "removeLink"})
        return

    if action == "wrap_tag":
        _run_js(web, {"op": "wrapTag", **(spec.arg or {})})
        return

    if action == "apply_style":
        _run_js(web, {"op": "applyStyle", "style": spec.arg or {}})
        return

    if action == "block_style":
        _run_js(web, {"op": "blockStyle", "style": spec.arg or {}})
        return

    if action == "indent":
        _run_js(web, {"op": "indent"})
        return

    if action == "outdent":
        _run_js(web, {"op": "outdent"})
        return

    if action == "insert_list":
        _run_js(web, {"op": "insertList", **(spec.arg or {})})
        return

    if action == "insert_blockquote":
        _run_js(web, {"op": "insertBlockquote"})
        return

    if action == "select_all":
        _run_js(web, {"op": "selectAll"})
        return

    if action == "clear_style_properties":
        _run_js(web, {"op": "clearStyleProperties", "properties": list(spec.arg or [])})
        return

    if action == "clear_format":
        _run_js(web, {"op": "clearFormat"})
        return


def dispatch_user_word(web: AnkiWebView, word: str) -> None:
    _insert_text(web, word)