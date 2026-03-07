from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from aqt.qt import QApplication, QFontDialog, QInputDialog
from aqt.utils import showInfo
from aqt.webview import AnkiWebView

from .menu_spec import CommandSpec


STYLE_WORD_TO_EDITOR_SIZE = {
    "x-small": 1,
    "small": 2,
    "medium": 3,
    "large": 4,
    "x-large": 5,
    "xx-large": 6,
    "xxx-large": 7,
}


WRAP_TAG_TO_EDITOR_COMMAND = {
    "b": "bold",
    "i": "italic",
    "u": "underline",
    "s": "strikethrough",
    "sup": "superscript",
    "sub": "subscript",
}


BLOCK_ALIGN_TO_EDITOR_COMMAND = {
    "left": "justifyLeft",
    "center": "justifyCenter",
    "right": "justifyRight",
    "justify": "justifyFull",
}


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


def _editor_eval(web: AnkiWebView, js: str) -> None:
    web.eval(js)


def _editor_set_format(web: AnkiWebView, command: str, value: Any | None = None) -> None:
    if value is None:
        js = f"setFormat({json.dumps(command)}); saveNow(1);"
    else:
        js = f"setFormat({json.dumps(command)}, {json.dumps(value, ensure_ascii=False)}); saveNow(1);"
    _editor_eval(web, js)


def _plain_text_to_html(text: str) -> str:
    return html.escape(text).replace("\r\n", "\n").replace("\n", "<br>")


def _insert_text_editor_native(web: AnkiWebView, text: str) -> None:
    _editor_set_format(web, "inserthtml", _plain_text_to_html(text))


def _insert_html_editor_native(web: AnkiWebView, raw_html: str) -> None:
    _editor_set_format(web, "inserthtml", raw_html)


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


def _paste_from_clipboard_editor_native(web: AnkiWebView) -> None:
    clipboard = QApplication.clipboard()
    mime = clipboard.mimeData()

    if mime is not None and mime.hasHtml():
        html_data = mime.html() or ""
        if html_data:
            _insert_html_editor_native(web, html_data)
            return

    _insert_text_editor_native(web, clipboard.text() or "")


def _paste_from_clipboard_reviewer(web: AnkiWebView) -> None:
    clipboard = QApplication.clipboard()
    mime = clipboard.mimeData()

    if mime is not None and mime.hasHtml():
        html_data = mime.html() or ""
        if html_data:
            _run_js(web, {"op": "insertHTML", "html": html_data})
            return

    _run_js(web, {"op": "insertText", "text": clipboard.text() or ""})


def _nearest_editor_font_size(point_size: int) -> int:
    if point_size <= 8:
        return 1
    if point_size <= 10:
        return 2
    if point_size <= 12:
        return 3
    if point_size <= 14:
        return 4
    if point_size <= 18:
        return 5
    if point_size <= 24:
        return 6
    return 7


def _apply_style_editor_native(web: AnkiWebView, style: dict[str, Any]) -> None:
    if not style:
        return

    if "fontWeight" in style and str(style["fontWeight"]).lower() == "bold":
        _editor_set_format(web, "bold")

    if "fontStyle" in style and str(style["fontStyle"]).lower() == "italic":
        _editor_set_format(web, "italic")

    if "textDecoration" in style:
        decoration = str(style["textDecoration"]).lower()
        if "underline" in decoration:
            _editor_set_format(web, "underline")
        if "line-through" in decoration:
            _editor_set_format(web, "strikethrough")

    if "color" in style:
        _editor_set_format(web, "forecolor", style["color"])

    if "backgroundColor" in style:
        _editor_set_format(web, "hilitecolor", style["backgroundColor"])

    if "fontSize" in style:
        size_value = style["fontSize"]
        editor_size = STYLE_WORD_TO_EDITOR_SIZE.get(str(size_value).lower())
        if editor_size:
            _editor_set_format(web, "fontsize", editor_size)

    if "fontFamily" in style:
        _editor_set_format(web, "fontname", style["fontFamily"])


def _dispatch_editor_native(web: AnkiWebView, spec: CommandSpec) -> bool:
    action = spec.action

    if action == "insert_text":
        _insert_text_editor_native(web, str(spec.arg))
        return True

    if action == "insert_html":
        _insert_html_editor_native(web, str(spec.arg))
        return True

    if action == "insert_datetime":
        _insert_text_editor_native(web, datetime.now().strftime(str(spec.arg)))
        return True

    if action == "insert_link_prompt":
        url, ok = QInputDialog.getText(None, "Insert Link", "URL:")
        if ok and url.strip():
            _editor_set_format(web, "createLink", url.strip())
        return True

    if action == "insert_image_prompt":
        url, ok = QInputDialog.getText(None, "Insert Image", "Image URL or path:")
        if ok and url.strip():
            src = _normalize_image_source(url)
            _insert_html_editor_native(web, f'<img src="{html.escape(src, quote=True)}">')
        return True

    if action == "font_dialog":
        font, ok = QFontDialog.getFont()
        if ok:
            _editor_set_format(web, "fontname", font.family())
            if font.pointSize() > 0:
                _editor_set_format(web, "fontsize", _nearest_editor_font_size(font.pointSize()))
            if font.bold():
                _editor_set_format(web, "bold")
            if font.italic():
                _editor_set_format(web, "italic")
            if font.underline():
                _editor_set_format(web, "underline")
            if font.strikeOut():
                _editor_set_format(web, "strikethrough")
        return True

    if action == "word_count":
        _run_js(
            web,
            {"op": "wordCount"},
            lambda result: showInfo(
                f"Words: {(result or {}).get('words', 0)}\n"
                f"Characters: {(result or {}).get('characters', 0)}"
            ),
        )
        return True

    if action == "copy":
        _run_js(
            web,
            {"op": "getSelectedText"},
            lambda result: QApplication.clipboard().setText(result or ""),
        )
        return True

    if action == "cut":
        _editor_set_format(web, "cut")
        return True

    if action == "paste":
        _paste_from_clipboard_editor_native(web)
        return True

    if action == "paste_plain_text":
        _insert_text_editor_native(web, QApplication.clipboard().text() or "")
        return True

    if action == "undo":
        _editor_set_format(web, "undo")
        return True

    if action == "redo":
        _editor_set_format(web, "redo")
        return True

    if action == "remove_link":
        _editor_set_format(web, "unlink")
        return True

    if action == "wrap_tag":
        tag = (spec.arg or {}).get("tag")
        command = WRAP_TAG_TO_EDITOR_COMMAND.get(tag)
        if command:
            _editor_set_format(web, command)
        return True

    if action == "apply_style":
        _apply_style_editor_native(web, dict(spec.arg or {}))
        return True

    if action == "block_style":
        style = dict(spec.arg or {})
        align = style.get("textAlign")
        command = BLOCK_ALIGN_TO_EDITOR_COMMAND.get(str(align))
        if command:
            _editor_set_format(web, command)
        return True

    if action == "indent":
        _editor_set_format(web, "indent")
        return True

    if action == "outdent":
        _editor_set_format(web, "outdent")
        return True

    if action == "insert_list":
        ordered = bool((spec.arg or {}).get("ordered"))
        _editor_set_format(web, "insertOrderedList" if ordered else "insertUnorderedList")
        return True

    if action == "insert_blockquote":
        _insert_html_editor_native(web, "<blockquote><br></blockquote>")
        return True

    if action == "select_all":
        _editor_set_format(web, "selectAll")
        return True

    if action == "clear_format":
        _editor_set_format(web, "removeFormat")
        return True

    return False


def dispatch_spec(web: AnkiWebView, spec: CommandSpec, context_name: str) -> None:
    if context_name == "editor" and _dispatch_editor_native(web, spec):
        return

    action = spec.action

    if action == "insert_text":
        _run_js(web, {"op": "insertText", "text": str(spec.arg)})
        return

    if action == "insert_html":
        _run_js(web, {"op": "insertHTML", "html": str(spec.arg)})
        return

    if action == "insert_datetime":
        _run_js(web, {"op": "insertText", "text": datetime.now().strftime(str(spec.arg))})
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
        _paste_from_clipboard_reviewer(web)
        return

    if action == "paste_plain_text":
        _run_js(web, {"op": "insertText", "text": QApplication.clipboard().text() or ""})
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

    if action == "clear_format":
        _run_js(web, {"op": "clearFormat"})
        return


def dispatch_user_word(web: AnkiWebView, word: str, context_name: str) -> None:
    if context_name == "editor":
        _insert_text_editor_native(web, word)
    else:
        _run_js(web, {"op": "insertText", "text": word})