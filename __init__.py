# GitHub: https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/

import json
from aqt import gui_hooks, mw
from aqt.qt import QAction
from aqt.editor import EditorWebView
from aqt.reviewer import Reviewer
from aqt.utils import showInfo, getText
from PyQt5.QtWidgets import QInputDialog, QFontDialog, QApplication, QMessageBox

import datetime

def getConfig():
    return mw.addonManager.getConfig(__name__)

def exec_command(web_instance, command, value=None):
    if value:
        cmd = f"document.execCommand('{command}', false, '{value}');"
    else:
        cmd = f"document.execCommand('{command}', false, null);"
    web_instance.eval(cmd)

def exec_command_with_js(web_instance, js_code):
    web_instance.eval(js_code)

def change_font_family(web_instance):
    font, ok = QFontDialog.getFont()
    if ok:
        family = font.family()
        cmd = f"document.execCommand('fontName', false, '{family}');"
        web_instance.eval(cmd)

def insert_special_character(web_instance, character):
    cmd = f"document.execCommand('insertText', false, '{character}');"
    web_instance.eval(cmd)

def insert_link(web_instance, url):
    if url:
        js_code = "document.execCommand('createLink', false, '{url}');"
        web_instance.eval(js_code.format(url=url))

def insert_image(web_instance, url):
    if url:
        js_code = "document.execCommand('insertImage', false, '{url}');"
        web_instance.eval(js_code.format(url=url))
"""
def insert_table(web_instance, rows, cols):
    table_html = "<table>"
    for _ in range(rows):
        table_html += "<tr>"
        for _ in range(cols):
            table_html += "<td></td>"
        table_html += "</tr>"
    table_html += "</table>"
    js_code = "document.execCommand('insertHTML', false, `{table_html}`);"
    web_instance.eval(js_code.format(table_html=table_html))
"""
def insert_date_and_time(web_instance, format_str):
    now = datetime.datetime.now()
    formatted_date = now.strftime(format_str)
    js_code = "document.execCommand('insertText', false, '{formatted_date}');"
    web_instance.eval(js_code.format(formatted_date=formatted_date))

def paste_plain_text(web_instance):
    clipboard = QApplication.clipboard()
    plain_text = clipboard.text()
    js_code = f"""
        var plainText = {json.dumps(plain_text)};
        var range;
        var sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {{
            range = sel.getRangeAt(0);
            range.deleteContents();
            var textNode = document.createTextNode(plainText);
            range.insertNode(textNode);
            range.setStartAfter(textNode);
            sel.removeAllRanges();
            sel.addRange(range);
        }}
    """
    exec_command_with_js(web_instance, js_code)

def paste_html(web_instance):
    clipboard = QApplication.clipboard()
    mime_data = clipboard.mimeData()
    if mime_data.hasHtml():
        html_content = mime_data.html()
        js_code = f'document.execCommand("insertHTML", false, {json.dumps(html_content)});'
        web_instance.eval(js_code)

def count_words_characters(web_instance):
    js_code = """
        (function() {{
            const selection = window.getSelection();
            const text = selection.toString().trim();
            if (text.length === 0) {{
                return [0, 0, 0];
            }} else {{
                const words = text.split(/\s+/).length;
                const characters_including_spaces = text.length;
                const characters_excluding_spaces = text.replace(/\s+/g, '').length;
                return [words, characters_including_spaces, characters_excluding_spaces];
            }}
        }})()
    """
    result = web_instance.page().runJavaScript(js_code, on_done)

def on_done(result):
    if result:
        words, characters_including_spaces, characters_excluding_spaces = result
        QMessageBox.information(None, "Word and Character Count", f"Words: {words}\nCharacters (including spaces): {characters_including_spaces}\nCharacters (excluding spaces): {characters_excluding_spaces}")
    else:
        QMessageBox.information(None, "Word and Character Count", "No text selected.")

def build_selection_menu(web_instance, menu, config):
    if config["enabled"]:
        selection_menu = menu.addMenu("Format / Edit")

        # Quick Access
        basic_actions = [
            ("Red", "foreColor", "red"),
            ("Subscript", "subscript", None),
            ("Strikethrough", "strikeThrough", None),
            ("Underline", "underline", None),
            ("YYYY-MM-DD HH:mm", "%Y-%m-%d %H:%M", None),
            ("(Clear Format)", "removeFormat", None),
        ]

        for action_name, command, value in basic_actions:
            action = QAction(action_name, menu)
            if action_name == "YYYY-MM-DD HH:mm":
                action.triggered.connect(lambda _, w=web_instance, c=command: insert_date_and_time(w, c))
                selection_menu.addAction(action)               
            else:
                action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
                selection_menu.addAction(action)

        # (Separator line)
        selection_menu.addSeparator()

        # Text Styling family
        text_styling_menu = selection_menu.addMenu("Text Styling")
        text_styling_actions = [
            ("Bold", "bold", None),
            ("Italic", "italic", None),
            ("Underline", "underline", None),
            ("Strikethrough", "strikeThrough", None),
            ("Superscript", "superscript", None),
            ("Subscript", "subscript", None),
        ]

        for action_name, command, value in text_styling_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            text_styling_menu.addAction(action)

        # Text Color family
        text_color_menu = selection_menu.addMenu("Text Color")
        text_color_actions = [
            ("Red", "foreColor", "red"),
            ("Green", "foreColor", "green"),
            ("Blue", "foreColor", "blue"),
            ("Cyan", "foreColor", "cyan"),
            ("Magenta", "foreColor", "magenta"),
            ("Yellow", "foreColor", "yellow"),
            ("Black", "foreColor", "black"),
            ("White", "foreColor", "white"),
            ("backRed", "backColor", "red"),
            ("backGreen", "backColor", "green"),
            ("backBlue", "backColor", "blue"),
            ("backCyan", "backColor", "cyan"),
            ("backMagenta", "backColor", "magenta"),
            ("backYellow", "backColor", "yellow"),
            ("backBlack", "backColor", "black"),
            ("backWhite", "backColor", "white"),
        ]

        for action_name, command, value in text_color_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            text_color_menu.addAction(action)

        # Font Size family
        font_size_menu = selection_menu.addMenu("Font Size")
        font_size_actions = [
            ("1", "fontSize", "1"),
            ("2", "fontSize", "2"),
            ("3", "fontSize", "3"),
            ("4", "fontSize", "4"),
            ("5", "fontSize", "5"),
            ("6", "fontSize", "6"),
            ("7", "fontSize", "7"),
        ]

        for action_name, command, value in font_size_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            font_size_menu.addAction(action)

        # Font...
        font_family_action = QAction("Font...", menu)
        font_family_action.triggered.connect(lambda _, w=web_instance: change_font_family(w))
        selection_menu.addAction(font_family_action)

        # (Separator line)
        selection_menu.addSeparator()

        # Alignment & Lists family
        alignment_menu = selection_menu.addMenu("Alignment / Lists")
        alignment_actions = [
            ("Justify Left", "justifyLeft", None),
            ("Justify Center", "justifyCenter", None),
            ("Justify Right", "justifyRight", None),
            ("Justify Full", "justifyFull", None),
            ("Indent", "indent", None),
            ("Outdent", "outdent", None),
            ("Insert Unordered List", "insertUnorderedList", None),
            ("Insert Ordered List", "insertOrderedList", None),
        ]

        for action_name, command, value in alignment_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            alignment_menu.addAction(action)

        # Words/Characters count
        count_action = QAction("Word Count", mw)
        count_action.triggered.connect(lambda _, w=web_instance: count_words_characters(w))
        selection_menu.addAction(count_action)

        # Insert family
        insert_menu = selection_menu.addMenu("Insert")

            # Insert link
        action = QAction("Insert Link", menu)
        action.triggered.connect(lambda _, w=web_instance: insert_link(w, getText("URL:")[0]))
        insert_menu.addAction(action)

            # Insert image
        def insert_image(web_instance, url):
            if url:
                js_code = "document.execCommand('insertImage', false, '{url}');"
                web_instance.eval(js_code.format(url=url))

        action = QAction("Insert Image", menu)
        action.triggered.connect(lambda _, w=web_instance: insert_image(w, getText("Image URL:")[0]))
        insert_menu.addAction(action)
        """
            # Insert table
        action = QAction("Insert Table", menu)
        action.triggered.connect(lambda _, w=web_instance: insert_table(w, int(getText("Rows:")[0]), int(getText("Columns:")[0])))
        insert_menu.addAction(action)
        """
            # Insert blockquote
        action = QAction("Insert Blockquote", menu)
        action.triggered.connect(lambda _, w=web_instance: exec_command(w, "formatBlock", "blockquote"))
        insert_menu.addAction(action)

            # Insert date and time
        date_and_time_menu = insert_menu.addMenu("Insert Date and Time")
        date_and_time_formats = [
            ("%Y-%m-%d", "YYYY-MM-DD"),
            ("%m/%d/%Y", "MM/DD/YYYY"),
            ("%B %d, %Y", "Month DD, YYYY"),
            ("%A, %B %d, %Y", "Day, Month DD, YYYY"),
            ("%I:%M %p", "hh:mm AM/PM"),
            ("%H:%M", "HH:mm"),
            ("%Y-%m-%d %H:%M", "YYYY-MM-DD HH:mm"),
        ]

        for format_str, display_format in date_and_time_formats:
            action = QAction(display_format, menu)
            action.triggered.connect(lambda _, w=web_instance, f=format_str: insert_date_and_time(w, f))
            date_and_time_menu.addAction(action)

            # Insert horizontal line
        action = QAction("Insert Horizontal Line", menu)
        action.triggered.connect(lambda _, w=web_instance: exec_command(w, "insertHorizontalRule", None))
        insert_menu.addAction(action)

            # Special Characters family
        special_characters_menu = insert_menu.addMenu("Insert Special Characters")
        special_characters_actions = [
            ("Em Dash (—)", "—"),
            ("En Dash (–)", "–"),
            ("Horizontal Bar (―)", "―"),
            ("Double Low Line (‗)", "‗"),
            ("Bullet (•)", "•"),
            ("Section (§)", "§"),
            ("Pilcrow (¶)", "¶"),
            ("Inverted ? (¿)", "¿"),
            ("Not (¬)", "¬"),
            ("Degree (°)", "°"),
            ("Micro (µ)", "µ"),
            ("+- (±)", "±"),
            ("Division (÷)", "÷"),
            ("Copyright (©)", "©"),
            ("Registered (®)", "®"),
            ("Trademark (™)", "™"),
            ("Euro (€)", "€"),
            ("Yen/Yuan (¥)", "¥"),
            ("Pound (£)", "£"),
            ("Cent (¢)", "¢"),
        ]

        for action_name, character in special_characters_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=character: insert_special_character(w, c))
            special_characters_menu.addAction(action)

        special_characters_sub_menu = special_characters_menu.addMenu("<3")
        special_characters_sub_actions = [
            ("♥","♥"),
            ("♡","♡"),
            ("❤","❤"),
            ("❥","❥"),
            ("❣","❣"),
            ("❦","❦"),
            ("❧","❧"),
            ("💗","💗"),
            ("💓","💓"),
            ("💔","💔"),
            ("💕","💕"),
            ("💖","💖"),
            ("💗","💗"),
            ("💘","💘"),
            ("💙","💙"),
            ("💚","💚"),
            ("💛","💛"),
            ("💜","💜"),
            ("💝","💝"),
            ("💞","💞"),
            ("💟","💟"),
            ("ღ","ღ"),
            ("ও","ও"),
        ]

        for action_name, character in special_characters_sub_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=character: insert_special_character(w, c))
            special_characters_sub_menu.addAction(action)

        # (Separator line)
        selection_menu.addSeparator()

        # Edit functions
        edit_functions_menu = selection_menu.addMenu("Edit")
        edit_actions = [
            ("Cut", "cut", None),
            ("Copy", "copy", None),
            ("Paste Plain Text", None, None),
            ("Paste Text/HTML", None, None),
            ("Select All", "selectAll", None),
            ("Undo", "undo", None),
            ("Redo", "redo", None),
        ]

        for action_name, command, value in edit_actions:
            action = QAction(action_name, menu)
            if action_name == "Paste Plain Text":
                action.triggered.connect(lambda _, w=web_instance: paste_plain_text(w))
            elif action_name == "Paste Text/HTML":
                action.triggered.connect(lambda _, w=web_instance: paste_html(w))
            else:
                action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            edit_functions_menu.addAction(action)

        # Add more parent items and actions here

def on_editor_context_menu(webview: EditorWebView, menu):
    web_instance = webview.editor.web
    config = getConfig()["editor"]
    build_selection_menu(web_instance, menu, config)

def on_reviewer_context_menu(webview, menu):
    reviewer = webview.parent().parent()
    web_instance = reviewer.web
    config = getConfig()["reviewer"]
    build_selection_menu(web_instance, menu, config)

# Add more context menu hooks here

gui_hooks.editor_will_show_context_menu.append(on_editor_context_menu)
gui_hooks.webview_will_show_context_menu.append(on_reviewer_context_menu)
