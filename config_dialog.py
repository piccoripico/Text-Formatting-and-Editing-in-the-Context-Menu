from __future__ import annotations

from pathlib import Path

from aqt import mw
from aqt.qt import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    Qt,
)

from .config_store import ADDON_MODULE, load_config, save_config
from .menu_spec import QUICK_ACCESS_GROUPS


try:
    OK_BUTTON = QDialogButtonBox.StandardButton.Ok
    CANCEL_BUTTON = QDialogButtonBox.StandardButton.Cancel
    LINEEDIT_NORMAL = QLineEdit.EchoMode.Normal
    SIZEPOLICY_MAXIMUM = QSizePolicy.Policy.Maximum
    SIZEPOLICY_FIXED = QSizePolicy.Policy.Fixed
    SCROLLBAR_AS_NEEDED = Qt.ScrollBarPolicy.ScrollBarAsNeeded
    SCROLLBAR_ALWAYS_OFF = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft
    ALIGN_TOP = Qt.AlignmentFlag.AlignTop

    def exec_dialog(dialog: QDialog) -> int:
        return dialog.exec()
except AttributeError:
    OK_BUTTON = QDialogButtonBox.Ok
    CANCEL_BUTTON = QDialogButtonBox.Cancel
    LINEEDIT_NORMAL = QLineEdit.Normal
    SIZEPOLICY_MAXIMUM = QSizePolicy.Maximum
    SIZEPOLICY_FIXED = QSizePolicy.Fixed
    SCROLLBAR_AS_NEEDED = Qt.ScrollBarAsNeeded
    SCROLLBAR_ALWAYS_OFF = Qt.ScrollBarAlwaysOff
    ALIGN_LEFT = Qt.AlignLeft
    ALIGN_TOP = Qt.AlignTop

    def exec_dialog(dialog: QDialog) -> int:
        return dialog.exec_()


def register_config_action() -> None:
    mw.addonManager.setConfigAction(ADDON_MODULE, open_config_dialog)


def open_config_dialog() -> None:
    dialog = ConfigDialog(mw)
    exec_dialog(dialog)


class ConfigDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle("Context Menu Text Tools - Config")
        self.resize(980, 700)

        self.config = load_config()
        self.quick_access_checkboxes: list[QCheckBox] = []

        layout = QVBoxLayout(self)
        tabs = QTabWidget(self)
        self.general_tab = QWidget()
        self.user_words_tab = QWidget()

        tabs.addTab(self.general_tab, "General")
        tabs.addTab(self.user_words_tab, "User Words")
        layout.addWidget(tabs)

        self._build_general_tab()
        self._build_user_words_tab()

        button_box = QDialogButtonBox(OK_BUTTON | CANCEL_BUTTON)
        button_box.accepted.connect(self._save_and_close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _build_general_tab(self) -> None:
        outer = QVBoxLayout(self.general_tab)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        root = QVBoxLayout(content)

        box_show = QGroupBox("(1) Show 'Format / Edit'")
        box_show_layout = QVBoxLayout(box_show)

        self.editor_checkbox = QCheckBox("Show 'Format / Edit' in Editor context menu")
        self.editor_checkbox.setChecked(self.config.get("editor", {}).get("enabled", True))
        box_show_layout.addWidget(self.editor_checkbox)

        self.reviewer_checkbox = QCheckBox(
            "Show 'Format / Edit' in Reviewer context menu "
            "(Available with the add-on 'Edit Field During Review (Cloze)', excluding some features.)"
        )
        self.reviewer_checkbox.setChecked(self.config.get("reviewer", {}).get("enabled", True))
        box_show_layout.addWidget(self.reviewer_checkbox)

        root.addWidget(box_show)

        box_quick_access = QGroupBox("(2) Quick Access Items")
        box_quick_access_outer = QVBoxLayout(box_quick_access)

        quick_access_scroll = QScrollArea()
        quick_access_scroll.setWidgetResizable(False)
        quick_access_scroll.setHorizontalScrollBarPolicy(SCROLLBAR_AS_NEEDED)
        quick_access_scroll.setVerticalScrollBarPolicy(SCROLLBAR_ALWAYS_OFF)
        quick_access_scroll.setAlignment(ALIGN_LEFT | ALIGN_TOP)

        quick_access_container = QWidget()
        quick_access_layout = QHBoxLayout(quick_access_container)
        quick_access_layout.setContentsMargins(0, 0, 0, 0)
        quick_access_layout.setSpacing(12)
        try:
            quick_access_layout.setAlignment(ALIGN_LEFT | ALIGN_TOP)
        except Exception:
            pass

        selected_labels = set(self.config.get("selected_quick_access_items", []))

        for group_title, labels in QUICK_ACCESS_GROUPS:
            group_box = QGroupBox(group_title)
            group_layout = QVBoxLayout(group_box)

            for label in labels:
                checkbox = QCheckBox(label)
                checkbox.setChecked(label in selected_labels)
                group_layout.addWidget(checkbox)
                self.quick_access_checkboxes.append(checkbox)

            group_layout.addStretch(1)
            group_box.setSizePolicy(SIZEPOLICY_MAXIMUM, SIZEPOLICY_FIXED)
            quick_access_layout.addWidget(group_box, 0, ALIGN_TOP)

        quick_access_layout.addStretch(1)
        quick_access_container.adjustSize()

        quick_access_scroll.setWidget(quick_access_container)
        quick_access_scroll.setMinimumHeight(quick_access_container.sizeHint().height() + 8)

        box_quick_access_outer.addWidget(quick_access_scroll)
        root.addWidget(box_quick_access)

        box_position = QGroupBox("(3) Quick Access Position")
        box_position_layout = QVBoxLayout(box_position)

        self.quick_access_position_checkbox = QCheckBox(
            "Display the Quick Access items on the first level of the context menu"
        )
        self.quick_access_position_checkbox.setChecked(self.config.get("quick_access_position", False))
        box_position_layout.addWidget(self.quick_access_position_checkbox)

        root.addWidget(box_position)
        root.addStretch(1)

    def _build_user_words_tab(self) -> None:
        outer = QVBoxLayout(self.user_words_tab)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        root = QVBoxLayout(content)

        self.words_checkbox = QCheckBox("Show 'User Words' (the added words below) in the context menu")
        self.words_checkbox.setChecked(self.config.get("user_words_flag", False))
        root.addWidget(self.words_checkbox)

        button_row_1 = QHBoxLayout()
        self.add_words_button = QPushButton("Add")
        self.edit_words_button = QPushButton("Edit")
        self.remove_words_button = QPushButton("Remove")
        button_row_1.addWidget(self.add_words_button)
        button_row_1.addWidget(self.edit_words_button)
        button_row_1.addWidget(self.remove_words_button)
        root.addLayout(button_row_1)

        root.addWidget(QLabel("Word list:"))

        self.words_list_widget = QListWidget()
        for word in self.config.get("user_words", []):
            self.words_list_widget.addItem(word)
        root.addWidget(self.words_list_widget)

        button_row_2 = QHBoxLayout()
        self.up_button = QPushButton("Move Up")
        self.down_button = QPushButton("Move Down")
        button_row_2.addWidget(self.up_button)
        button_row_2.addWidget(self.down_button)
        root.addLayout(button_row_2)

        button_row_3 = QHBoxLayout()
        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        button_row_3.addWidget(self.import_button)
        button_row_3.addWidget(self.export_button)
        root.addLayout(button_row_3)

        self.words_position_checkbox = QCheckBox(
            "Display the added words on the first level of the context menu"
        )
        self.words_position_checkbox.setChecked(self.config.get("user_words_position", False))
        root.addWidget(self.words_position_checkbox)

        self.add_words_button.clicked.connect(self._add_word)
        self.edit_words_button.clicked.connect(self._edit_word)
        self.remove_words_button.clicked.connect(self._remove_word)
        self.up_button.clicked.connect(self._move_up)
        self.down_button.clicked.connect(self._move_down)
        self.import_button.clicked.connect(self._import_words)
        self.export_button.clicked.connect(self._export_words)

        root.addStretch(1)

    def _add_word(self) -> None:
        text, ok = QInputDialog.getText(self, "Add Word", "Enter the word:")
        if ok and text.strip():
            self.words_list_widget.addItem(text.strip())

    def _edit_word(self) -> None:
        item = self.words_list_widget.currentItem()
        if not item:
            return
        new_text, ok = QInputDialog.getText(
            self,
            "Edit Word",
            "New Word:",
            LINEEDIT_NORMAL,
            item.text(),
        )
        if ok and new_text.strip():
            item.setText(new_text.strip())

    def _remove_word(self) -> None:
        current_item = self.words_list_widget.currentItem()
        if current_item:
            self.words_list_widget.takeItem(self.words_list_widget.row(current_item))

    def _move_up(self) -> None:
        current_row = self.words_list_widget.currentRow()
        if current_row > 0:
            item = self.words_list_widget.takeItem(current_row)
            self.words_list_widget.insertItem(current_row - 1, item)
            self.words_list_widget.setCurrentRow(current_row - 1)

    def _move_down(self) -> None:
        current_row = self.words_list_widget.currentRow()
        if 0 <= current_row < self.words_list_widget.count() - 1:
            item = self.words_list_widget.takeItem(current_row)
            self.words_list_widget.insertItem(current_row + 1, item)
            self.words_list_widget.setCurrentRow(current_row + 1)

    def _import_words(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return

        text = Path(file_path).read_text(encoding="utf-8-sig")
        words = [line.strip() for line in text.splitlines() if line.strip()]

        self.words_list_widget.clear()
        self.words_list_widget.addItems(words)

    def _export_words(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "user_words.txt",
            "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return

        words = [self.words_list_widget.item(i).text() for i in range(self.words_list_widget.count())]
        Path(file_path).write_text("\n".join(words) + ("\n" if words else ""), encoding="utf-8")

    def _save_and_close(self) -> None:
        selected_quick_access_items = [
            checkbox.text() for checkbox in self.quick_access_checkboxes if checkbox.isChecked()
        ]
        user_words = [
            self.words_list_widget.item(i).text()
            for i in range(self.words_list_widget.count())
        ]

        self.config["editor"]["enabled"] = self.editor_checkbox.isChecked()
        self.config["reviewer"]["enabled"] = self.reviewer_checkbox.isChecked()
        self.config["selected_quick_access_items"] = selected_quick_access_items
        self.config["quick_access_position"] = self.quick_access_position_checkbox.isChecked()
        self.config["user_words_flag"] = self.words_checkbox.isChecked()
        self.config["user_words"] = user_words
        self.config["user_words_position"] = self.words_position_checkbox.isChecked()

        save_config(self.config)
        self.accept()