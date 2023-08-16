# Note: This addon uses a deprecated Javascript function "document.execCommand". Official changes to Javascript may affect this addon in the future.

import json, datetime
from aqt import gui_hooks, mw
from aqt.qt import *
from aqt.editor import EditorWebView, Editor
from aqt.reviewer import Reviewer
from aqt.utils import showInfo, getText
from PyQt5.QtWidgets import QInputDialog, QFontDialog, QApplication, QMessageBox, QFileDialog

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
    # unavailable if web_instance = reviewer.web
    if url:
        js_code = "document.execCommand('createLink', false, '{url}');"
        web_instance.eval(js_code.format(url=url))

def insert_image(web_instance, url):
    # unavailable if web_instance = reviewer.web
    if url:
        js_code = "document.execCommand('insertImage', false, '{url}');"
        web_instance.eval(js_code.format(url=url))

def insert_date_and_time(web_instance, format_str):
    now = datetime.datetime.now()
    formatted_date = now.strftime(format_str)
    js_code = "document.execCommand('insertText', false, '{formatted_date}');"
    web_instance.eval(js_code.format(formatted_date=formatted_date))

''' # unexpected behavior
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
'''

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
        config = getConfig()

        if config.get("user_words_flag") == True:
        # user words
            user_words = config.get("user_words", [])
            if user_words:
                user_words_actions = [(word, word) for word in user_words]

            ## user words on the first level or inside Format / Edit of the context menu
                if config.get("user_words_position") == True:
        # (Separator line)
                    menu.addSeparator()
                ### User Words
                    for action_name, character in user_words_actions:
                        action = QAction(action_name, menu)
                        action.triggered.connect(lambda _, w=web_instance, c=character: insert_special_character(w, c))
                        menu.addAction(action)
        # (Separator line)
                    menu.addSeparator()
                else:
                ### User Words
                    user_words_menu = selection_menu.addMenu("User Words")
                    for action_name, character in user_words_actions:
                        action = QAction(action_name, menu)
                        action.triggered.connect(lambda _, w=web_instance, c=character: insert_special_character(w, c))
                        user_words_menu.addAction(action)
        # (Separator line)
                    selection_menu.addSeparator()

        ### All items listed below ###
        # Quick Access
        quick_access_items = config.get("selected_quick_access_items", []) 
        basic_actions = [item for item in all_quick_access_items if item[0] in quick_access_items]

            ## Quick Access on the first level or inside Format / Edit of the context menu
        if config.get("quick_access_position") == True:
        # (Separator line)
            menu.addSeparator()
            for action_name, command, value in basic_actions:
                action = QAction(action_name, menu)
                if value == "TIME":
                    action.triggered.connect(lambda _, w=web_instance, c=command: insert_date_and_time(w, c))
                    menu.addAction(action)               
                else:
                    action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
                    menu.addAction(action)
        # (Separator line)
            menu.addSeparator()
        else:
        # (Separator line)
            selection_menu.addSeparator()
            for action_name, command, value in basic_actions:
                action = QAction(action_name, menu)
                if value == "TIME":
                    action.triggered.connect(lambda _, w=web_instance, c=command: insert_date_and_time(w, c))
                    selection_menu.addAction(action)               
                else:
                    action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
                    selection_menu.addAction(action)
        # (Separator line)
            selection_menu.addSeparator()

        # Text Styling family
        text_styling_menu = selection_menu.addMenu("Text Styling")
        for action_name, command, value in text_styling_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            text_styling_menu.addAction(action)

        # Text Color family
        text_color_menu = selection_menu.addMenu("Text Color")
        for action_name, command, value in text_color_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            text_color_menu.addAction(action)

        # Font Size family
        font_size_menu = selection_menu.addMenu("Font Size")
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
        alignment_menu = selection_menu.addMenu("Alignment / List")
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
        action = QAction("Insert Image", menu)
        action.triggered.connect(lambda _, w=web_instance: insert_image(w, getText("Image URL:")[0]))
        insert_menu.addAction(action)

            # Insert blockquote
        action = QAction("Insert Blockquote", menu)
        action.triggered.connect(lambda _, w=web_instance: exec_command(w, "formatBlock", "blockquote"))
        insert_menu.addAction(action)

            # Insert date and time
        date_and_time_menu = insert_menu.addMenu("Insert Date and Time")
        for display_format, format_str, time_label in date_and_time_formats:
            action = QAction(display_format, menu)
            action.triggered.connect(lambda _, w=web_instance, f=format_str: insert_date_and_time(w, f))
            date_and_time_menu.addAction(action)

            # Insert horizontal line
        action = QAction("Insert Horizontal Line", menu)
        action.triggered.connect(lambda _, w=web_instance: exec_command(w, "insertHorizontalRule", None))
        insert_menu.addAction(action)

            # Special Characters family
        special_characters_menu = insert_menu.addMenu("Insert Special Characters")
        for action_name, character in special_characters_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=character: insert_special_character(w, c))
            special_characters_menu.addAction(action)
        '''
        special_characters_sub_menu = special_characters_menu.addMenu("<3")
        for action_name, character in special_characters_sub_actions:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=character: insert_special_character(w, c))
            special_characters_sub_menu.addAction(action)
        '''
        # (Separator line)
        selection_menu.addSeparator()

        # Edit functions
        edit_functions_menu = selection_menu.addMenu("Edit")
        for action_name, command, value in edit_actions:
            action = QAction(action_name, menu)
            if action_name == "Paste Text/HTML":
                action.triggered.connect(lambda _, w=web_instance: paste_html(w))
            else:
                action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            edit_functions_menu.addAction(action)

        # (Clear Format)
        for action_name, command, value in clear_format:
            action = QAction(action_name, menu)
            action.triggered.connect(lambda _, w=web_instance, c=command, v=value: exec_command(w, c, v))
            selection_menu.addAction(action)

# All items
text_styling_actions = [
    ("Bold", "bold", None),
    ("Italic", "italic", None),
    ("Underline", "underline", None),
    ("Strikethrough", "strikeThrough", None),
    ("Superscript", "superscript", None),
    ("Subscript", "subscript", None),
]

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

font_size_actions = [
    ("Size 1", "fontSize", "1"),
    ("Size 2", "fontSize", "2"),
    ("Size 3", "fontSize", "3"),
    ("Size 4", "fontSize", "4"),
    ("Size 5", "fontSize", "5"),
    ("Size 6", "fontSize", "6"),
    ("Size 7", "fontSize", "7"),
]

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

date_and_time_formats = [
    ("YYYY-MM-DD", "%Y-%m-%d", "TIME"),
    ("MM/DD/YYYY", "%m/%d/%Y", "TIME"),
    ("Month DD, YYYY", "%B %d, %Y", "TIME"),
    ("Day, Month DD, YYYY", "%A, %B %d, %Y", "TIME"),
    ("hh:mm AM/PM", "%I:%M %p", "TIME"),
    ("HH:mm", "%H:%M", "TIME"),
    ("YYYY-MM-DD HH:mm", "%Y-%m-%d %H:%M", "TIME"),
]

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
'''
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
'''
edit_actions = [
    ("Cut", "cut", None),
    ("Copy", "copy", None),
    ("Paste Text/HTML", None, None),
    ("Select All", "selectAll", None),
    ("Undo", "undo", None),
    ("Redo", "redo", None),
]

clear_format = [
    ("(Clear Format)", "removeFormat", None),
]

all_quick_access_items = text_styling_actions + text_color_actions + font_size_actions + alignment_actions + date_and_time_formats + clear_format

# Context menus
def on_editor_context_menu(webview: EditorWebView, menu):
    web_instance = webview.editor.web
    config = getConfig()["editor"]
    build_selection_menu(web_instance, menu, config)

def on_reviewer_context_menu(webview, menu):
    reviewer = mw.reviewer
    web_instance = reviewer.web
    config = getConfig()["reviewer"]
    build_selection_menu(web_instance, menu, config)

gui_hooks.editor_will_show_context_menu.append(on_editor_context_menu)
gui_hooks.webview_will_show_context_menu.append(on_reviewer_context_menu)