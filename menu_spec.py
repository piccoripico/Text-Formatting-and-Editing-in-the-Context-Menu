from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

CTX_BOTH = frozenset({"editor", "reviewer"})


@dataclass(frozen=True)
class CommandSpec:
    id: str
    label: str
    action: str
    arg: Any = None
    category: str = ""
    submenu: str | None = None
    contexts: frozenset[str] = field(default_factory=lambda: CTX_BOTH)
    quick_access_allowed: bool = False


def cmd(
    id: str,
    label: str,
    action: str,
    arg: Any = None,
    *,
    category: str,
    submenu: str | None = None,
    contexts: frozenset[str] = CTX_BOTH,
    quick_access_allowed: bool = False,
) -> CommandSpec:
    return CommandSpec(
        id=id,
        label=label,
        action=action,
        arg=arg,
        category=category,
        submenu=submenu,
        contexts=contexts,
        quick_access_allowed=quick_access_allowed,
    )


COMMANDS: list[CommandSpec] = [
    # Text Styling
    cmd("bold", "Bold", "wrap_tag", {"tag": "b"}, category="text_styling", quick_access_allowed=True),
    cmd("italic", "Italic", "wrap_tag", {"tag": "i"}, category="text_styling", quick_access_allowed=True),
    cmd("underline", "Underline", "wrap_tag", {"tag": "u"}, category="text_styling", quick_access_allowed=True),
    cmd("strikethrough", "Strikethrough", "wrap_tag", {"tag": "s"}, category="text_styling", quick_access_allowed=True),
    cmd("superscript", "Superscript", "wrap_tag", {"tag": "sup"}, category="text_styling", quick_access_allowed=True),
    cmd("subscript", "Subscript", "wrap_tag", {"tag": "sub"}, category="text_styling", quick_access_allowed=True),

    # Text Color
    cmd("red", "Red", "apply_style", {"color": "red"}, category="text_color", quick_access_allowed=True),
    cmd("green", "Green", "apply_style", {"color": "green"}, category="text_color", quick_access_allowed=True),
    cmd("blue", "Blue", "apply_style", {"color": "blue"}, category="text_color", quick_access_allowed=True),
    cmd("cyan", "Cyan", "apply_style", {"color": "cyan"}, category="text_color", quick_access_allowed=True),
    cmd("magenta", "Magenta", "apply_style", {"color": "magenta"}, category="text_color", quick_access_allowed=True),
    cmd("yellow", "Yellow", "apply_style", {"color": "yellow"}, category="text_color", quick_access_allowed=True),
    cmd("black", "Black", "apply_style", {"color": "black"}, category="text_color", quick_access_allowed=True),
    cmd("white", "White", "apply_style", {"color": "white"}, category="text_color", quick_access_allowed=True),

    cmd("back_red", "Highlight Red", "apply_style", {"backgroundColor": "red"}, category="text_color", quick_access_allowed=True),
    cmd("back_green", "Highlight Green", "apply_style", {"backgroundColor": "green"}, category="text_color", quick_access_allowed=True),
    cmd("back_blue", "Highlight Blue", "apply_style", {"backgroundColor": "blue"}, category="text_color", quick_access_allowed=True),
    cmd("back_cyan", "Highlight Cyan", "apply_style", {"backgroundColor": "cyan"}, category="text_color", quick_access_allowed=True),
    cmd("back_magenta", "Highlight Magenta", "apply_style", {"backgroundColor": "magenta"}, category="text_color", quick_access_allowed=True),
    cmd("back_yellow", "Highlight Yellow", "apply_style", {"backgroundColor": "yellow"}, category="text_color", quick_access_allowed=True),
    cmd("back_black", "Highlight Black", "apply_style", {"backgroundColor": "black"}, category="text_color", quick_access_allowed=True),
    cmd("back_white", "Highlight White", "apply_style", {"backgroundColor": "white"}, category="text_color", quick_access_allowed=True),

    # Font Size
    cmd("size_1", "Size 1", "apply_style", {"fontSize": "x-small"}, category="font_size", quick_access_allowed=True),
    cmd("size_2", "Size 2", "apply_style", {"fontSize": "small"}, category="font_size", quick_access_allowed=True),
    cmd("size_3", "Size 3", "apply_style", {"fontSize": "medium"}, category="font_size", quick_access_allowed=True),
    cmd("size_4", "Size 4", "apply_style", {"fontSize": "large"}, category="font_size", quick_access_allowed=True),
    cmd("size_5", "Size 5", "apply_style", {"fontSize": "x-large"}, category="font_size", quick_access_allowed=True),
    cmd("size_6", "Size 6", "apply_style", {"fontSize": "xx-large"}, category="font_size", quick_access_allowed=True),
    cmd("size_7", "Size 7", "apply_style", {"fontSize": "xxx-large"}, category="font_size", quick_access_allowed=True),

    # Font
    cmd("font_dialog", "Font...", "font_dialog", category="font"),

    # Style Presets
    cmd(
        "preset_strong_emphasis",
        "Strong Emphasis (Bold + Underline)",
        "apply_style",
        {"fontWeight": "bold", "textDecoration": "underline"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_important",
        "Important (Bold + Red)",
        "apply_style",
        {"fontWeight": "bold", "color": "red"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_key_point",
        "Key Point (Bold + Yellow Highlight)",
        "apply_style",
        {"fontWeight": "bold", "backgroundColor": "yellow"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_alert",
        "Alert (Bold + Red + Yellow Highlight)",
        "apply_style",
        {"fontWeight": "bold", "color": "red", "backgroundColor": "yellow"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_underlined_attention",
        "Underlined Attention (Underline + Red)",
        "apply_style",
        {"textDecoration": "underline", "color": "red"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_blue_emphasis",
        "Blue Emphasis (Bold + Blue)",
        "apply_style",
        {"fontWeight": "bold", "color": "blue"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_green_emphasis",
        "Green Emphasis (Bold + Green)",
        "apply_style",
        {"fontWeight": "bold", "color": "green"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_marked_attention",
        "Marked Attention (Bold + Magenta)",
        "apply_style",
        {"fontWeight": "bold", "color": "magenta"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_heading_large",
        "Heading Large (Bold + Size 5)",
        "apply_style",
        {"fontWeight": "bold", "fontSize": "x-large"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_large_emphasis",
        "Large Emphasis (Bold + Red + Size 5)",
        "apply_style",
        {"fontWeight": "bold", "color": "red", "fontSize": "x-large"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_side_note",
        "Side Note (Cyan + Size 2)",
        "apply_style",
        {"color": "cyan", "fontSize": "small"},
        category="style_presets",
        quick_access_allowed=True,
    ),

    # Alignment / List
    cmd("justify_left", "Justify Left", "block_style", {"textAlign": "left"}, category="alignment", quick_access_allowed=True),
    cmd("justify_center", "Justify Center", "block_style", {"textAlign": "center"}, category="alignment", quick_access_allowed=True),
    cmd("justify_right", "Justify Right", "block_style", {"textAlign": "right"}, category="alignment", quick_access_allowed=True),
    cmd("justify_full", "Justify Full", "block_style", {"textAlign": "justify"}, category="alignment", quick_access_allowed=True),
    cmd("indent", "Indent", "indent", category="alignment", quick_access_allowed=True),
    cmd("outdent", "Outdent", "outdent", category="alignment", quick_access_allowed=True),
    cmd("insert_unordered_list", "Insert Unordered List", "insert_list", {"ordered": False}, category="alignment", quick_access_allowed=True),
    cmd("insert_ordered_list", "Insert Ordered List", "insert_list", {"ordered": True}, category="alignment", quick_access_allowed=True),

    # Tools
    cmd("word_count", "Word Count", "word_count", category="tools"),

    # Insert
    cmd("insert_link", "Insert Link", "insert_link_prompt", category="insert"),
    cmd("insert_image", "Insert Image", "insert_image_prompt", category="insert"),
    cmd("insert_blockquote", "Insert Blockquote", "insert_blockquote", category="insert"),
    cmd("insert_horizontal_rule", "Insert Horizontal Line", "insert_html", "<hr>", category="insert"),

    cmd("date_ymd", "YYYY-MM-DD", "insert_datetime", "%Y-%m-%d", category="insert", submenu="Insert Date and Time", quick_access_allowed=True),
    cmd("date_mdy", "MM/DD/YYYY", "insert_datetime", "%m/%d/%Y", category="insert", submenu="Insert Date and Time", quick_access_allowed=True),
    cmd("date_month_dd_yyyy", "Month DD, YYYY", "insert_datetime", "%B %d, %Y", category="insert", submenu="Insert Date and Time", quick_access_allowed=True),
    cmd("date_day_month_dd_yyyy", "Day, Month DD, YYYY", "insert_datetime", "%A, %B %d, %Y", category="insert", submenu="Insert Date and Time", quick_access_allowed=True),
    cmd("time_ampm", "hh:mm AM/PM", "insert_datetime", "%I:%M %p", category="insert", submenu="Insert Date and Time", quick_access_allowed=True),
    cmd("time_24h", "HH:mm", "insert_datetime", "%H:%M", category="insert", submenu="Insert Date and Time", quick_access_allowed=True),
    cmd("datetime_ymd_hm", "YYYY-MM-DD HH:mm", "insert_datetime", "%Y-%m-%d %H:%M", category="insert", submenu="Insert Date and Time", quick_access_allowed=True),

    cmd("special_em_dash", "Em Dash (—)", "insert_text", "—", category="insert", submenu="Insert Special Characters"),
    cmd("special_en_dash", "En Dash (–)", "insert_text", "–", category="insert", submenu="Insert Special Characters"),
    cmd("special_hbar", "Horizontal Bar (―)", "insert_text", "―", category="insert", submenu="Insert Special Characters"),
    cmd("special_double_low_line", "Double Low Line (‗)", "insert_text", "‗", category="insert", submenu="Insert Special Characters"),
    cmd("special_bullet", "Bullet (•)", "insert_text", "•", category="insert", submenu="Insert Special Characters"),
    cmd("special_section", "Section (§)", "insert_text", "§", category="insert", submenu="Insert Special Characters"),
    cmd("special_pilcrow", "Pilcrow (¶)", "insert_text", "¶", category="insert", submenu="Insert Special Characters"),
    cmd("special_inverted_q", "Inverted ? (¿)", "insert_text", "¿", category="insert", submenu="Insert Special Characters"),
    cmd("special_not", "Not (¬)", "insert_text", "¬", category="insert", submenu="Insert Special Characters"),
    cmd("special_degree", "Degree (°)", "insert_text", "°", category="insert", submenu="Insert Special Characters"),
    cmd("special_micro", "Micro (µ)", "insert_text", "µ", category="insert", submenu="Insert Special Characters"),
    cmd("special_plus_minus", "+- (±)", "insert_text", "±", category="insert", submenu="Insert Special Characters"),
    cmd("special_division", "Division (÷)", "insert_text", "÷", category="insert", submenu="Insert Special Characters"),
    cmd("special_copyright", "Copyright (©)", "insert_text", "©", category="insert", submenu="Insert Special Characters"),
    cmd("special_registered", "Registered (®)", "insert_text", "®", category="insert", submenu="Insert Special Characters"),
    cmd("special_trademark", "Trademark (™)", "insert_text", "™", category="insert", submenu="Insert Special Characters"),
    cmd("special_euro", "Euro (€)", "insert_text", "€", category="insert", submenu="Insert Special Characters"),
    cmd("special_yen", "Yen/Yuan (¥)", "insert_text", "¥", category="insert", submenu="Insert Special Characters"),
    cmd("special_pound", "Pound (£)", "insert_text", "£", category="insert", submenu="Insert Special Characters"),
    cmd("special_cent", "Cent (¢)", "insert_text", "¢", category="insert", submenu="Insert Special Characters"),

    # Edit
    cmd("cut", "Cut", "cut", category="edit"),
    cmd("copy", "Copy", "copy", category="edit"),
    cmd("paste", "Paste", "paste", category="edit"),
    cmd("paste_plain_text", "Paste Plain Text", "paste_plain_text", category="edit"),
    cmd("remove_link", "Remove Link", "remove_link", category="edit"),
    cmd("select_all", "Select All", "select_all", category="edit"),
    cmd("undo", "Undo", "undo", category="edit"),
    cmd("redo", "Redo", "redo", category="edit"),

    # Clear helpers
    cmd("clear_text_color", "Clear Text Color", "clear_style_properties", ["color"], category="clear_format"),
    cmd("clear_highlight", "Clear Highlight", "clear_style_properties", ["backgroundColor"], category="clear_format"),
    cmd("clear_format", "Clear All Formatting", "clear_format", category="clear_format", quick_access_allowed=True),
]

LABEL_TO_SPEC: dict[str, CommandSpec] = {spec.label: spec for spec in COMMANDS}

STYLE_PRESET_SECTIONS: list[list[str]] = [
    [
        "Strong Emphasis (Bold + Underline)",
        "Important (Bold + Red)",
        "Key Point (Bold + Yellow Highlight)",
        "Alert (Bold + Red + Yellow Highlight)",
        "Underlined Attention (Underline + Red)",
    ],
    [
        "Blue Emphasis (Bold + Blue)",
        "Green Emphasis (Bold + Green)",
        "Marked Attention (Bold + Magenta)",
    ],
    [
        "Heading Large (Bold + Size 5)",
        "Large Emphasis (Bold + Red + Size 5)",
        "Side Note (Cyan + Size 2)",
    ],
]

QUICK_ACCESS_GROUPS: list[tuple[str, list[str]]] = [
    (
        "Text Styling",
        ["Bold", "Italic", "Underline", "Strikethrough", "Superscript", "Subscript"],
    ),
    (
        "Text Color",
        [
            "Red", "Green", "Blue", "Cyan", "Magenta", "Yellow", "Black", "White",
            "Highlight Red", "Highlight Green", "Highlight Blue", "Highlight Cyan",
            "Highlight Magenta", "Highlight Yellow", "Highlight Black", "Highlight White",
        ],
    ),
    (
        "Font Size",
        ["Size 1", "Size 2", "Size 3", "Size 4", "Size 5", "Size 6", "Size 7"],
    ),
    (
        "Style Presets",
        [
            "Strong Emphasis (Bold + Underline)",
            "Important (Bold + Red)",
            "Key Point (Bold + Yellow Highlight)",
            "Alert (Bold + Red + Yellow Highlight)",
            "Underlined Attention (Underline + Red)",
            "Blue Emphasis (Bold + Blue)",
            "Green Emphasis (Bold + Green)",
            "Marked Attention (Bold + Magenta)",
            "Heading Large (Bold + Size 5)",
            "Large Emphasis (Bold + Red + Size 5)",
            "Side Note (Cyan + Size 2)",
        ],
    ),
    (
        "Alignment / List",
        [
            "Justify Left", "Justify Center", "Justify Right", "Justify Full",
            "Indent", "Outdent", "Insert Unordered List", "Insert Ordered List",
        ],
    ),
    (
        "Date / Time",
        [
            "YYYY-MM-DD",
            "MM/DD/YYYY",
            "Month DD, YYYY",
            "Day, Month DD, YYYY",
            "hh:mm AM/PM",
            "HH:mm",
            "YYYY-MM-DD HH:mm",
        ],
    ),
    (
        "Clear Formatting",
        ["Clear All Formatting"],
    ),
]