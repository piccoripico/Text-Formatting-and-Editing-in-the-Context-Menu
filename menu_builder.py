from __future__ import annotations

from aqt.qt import QAction, QMenu
from aqt.webview import AnkiWebView

from .actions import dispatch_spec, dispatch_user_word
from .config_store import load_config
from .menu_spec import COMMANDS, LABEL_TO_SPEC, CommandSpec, STYLE_PRESET_SECTIONS


def _add_action(menu: QMenu, label: str, callback) -> None:
    action = QAction(label, menu)
    action.triggered.connect(callback)
    menu.addAction(action)


def _specs_for_context(context_name: str) -> list[CommandSpec]:
    return [spec for spec in COMMANDS if context_name in spec.contexts]


def _spec_by_label_for_context(context_name: str, label: str) -> CommandSpec | None:
    spec = LABEL_TO_SPEC.get(label)
    if spec and context_name in spec.contexts:
        return spec
    return None


def _add_spec_action(menu: QMenu, web: AnkiWebView, spec: CommandSpec) -> None:
    _add_action(menu, spec.label, lambda _checked=False, s=spec: dispatch_spec(web, s))


def _submenu_specs(context_name: str, category: str, submenu: str | None = None) -> list[CommandSpec]:
    specs = _specs_for_context(context_name)
    return [spec for spec in specs if spec.category == category and spec.submenu == submenu]


def _quick_access_specs(config: dict, context_name: str) -> list[CommandSpec]:
    specs: list[CommandSpec] = []
    for label in config.get("selected_quick_access_items", []):
        spec = _spec_by_label_for_context(context_name, label)
        if spec and spec.quick_access_allowed:
            specs.append(spec)
    return specs


def _build_user_words(config: dict, parent_menu: QMenu, root_menu: QMenu, web: AnkiWebView) -> None:
    if not config.get("user_words_flag", False):
        return

    user_words = config.get("user_words", [])
    if not user_words:
        return

    if config.get("user_words_position", False):
        parent_menu.addSeparator()
        for word in user_words:
            _add_action(
                parent_menu,
                word,
                lambda _checked=False, w=word: dispatch_user_word(web, w),
            )
    else:
        user_words_menu = root_menu.addMenu("User Words")
        for word in user_words:
            _add_action(
                user_words_menu,
                word,
                lambda _checked=False, w=word: dispatch_user_word(web, w),
            )


def build_context_menu(parent_menu: QMenu, context_name: str, web: AnkiWebView) -> None:
    config = load_config()
    quick_specs = _quick_access_specs(config, context_name)

    quick_access_on_first_level = bool(config.get("quick_access_position", False))
    if quick_access_on_first_level and quick_specs:
        for spec in quick_specs:
            _add_spec_action(parent_menu, web, spec)
        parent_menu.addSeparator()

    root_menu = parent_menu.addMenu("Format / Edit")

    if (not quick_access_on_first_level) and quick_specs:
        for spec in quick_specs:
            _add_spec_action(root_menu, web, spec)
        root_menu.addSeparator()

    # Text Styling
    text_styling_menu = root_menu.addMenu("Text Styling")
    for spec in _submenu_specs(context_name, "text_styling"):
        _add_spec_action(text_styling_menu, web, spec)

    # Text Color
    text_color_menu = root_menu.addMenu("Text Color")
    for spec in _submenu_specs(context_name, "text_color"):
        _add_spec_action(text_color_menu, web, spec)

    # Font Size
    font_size_menu = root_menu.addMenu("Font Size")
    for spec in _submenu_specs(context_name, "font_size"):
        _add_spec_action(font_size_menu, web, spec)

    # Font...
    font_spec = _spec_by_label_for_context(context_name, "Font...")
    if font_spec:
        _add_spec_action(root_menu, web, font_spec)

    # Style Presets
    style_presets_menu = root_menu.addMenu("Style Presets")
    for section_index, section in enumerate(STYLE_PRESET_SECTIONS):
        if section_index > 0:
            style_presets_menu.addSeparator()
        for label in section:
            spec = _spec_by_label_for_context(context_name, label)
            if spec:
                _add_spec_action(style_presets_menu, web, spec)

    root_menu.addSeparator()

    # Alignment / List
    alignment_menu = root_menu.addMenu("Alignment / List")
    for spec in _submenu_specs(context_name, "alignment"):
        _add_spec_action(alignment_menu, web, spec)

    # Word Count
    word_count_spec = _spec_by_label_for_context(context_name, "Word Count")
    if word_count_spec:
        _add_spec_action(root_menu, web, word_count_spec)

    # Insert
    insert_menu = root_menu.addMenu("Insert")

    for label in ["Insert Link", "Insert Image", "Insert Blockquote"]:
        spec = _spec_by_label_for_context(context_name, label)
        if spec:
            _add_spec_action(insert_menu, web, spec)

    date_time_menu = insert_menu.addMenu("Insert Date and Time")
    for spec in _submenu_specs(context_name, "insert", "Insert Date and Time"):
        _add_spec_action(date_time_menu, web, spec)

    horizontal_rule_spec = _spec_by_label_for_context(context_name, "Insert Horizontal Line")
    if horizontal_rule_spec:
        _add_spec_action(insert_menu, web, horizontal_rule_spec)

    special_characters_menu = insert_menu.addMenu("Insert Special Characters")
    for spec in _submenu_specs(context_name, "insert", "Insert Special Characters"):
        _add_spec_action(special_characters_menu, web, spec)

    root_menu.addSeparator()

    # Edit
    edit_menu = root_menu.addMenu("Edit")
    for spec in _submenu_specs(context_name, "edit"):
        _add_spec_action(edit_menu, web, spec)

    root_menu.addSeparator()

    # Clear helpers
    for label in ["Clear Text Color", "Clear Highlight", "Clear All Formatting"]:
        spec = _spec_by_label_for_context(context_name, label)
        if spec:
            _add_spec_action(root_menu, web, spec)

    # User Words
    _build_user_words(config, parent_menu, root_menu, web)