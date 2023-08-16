from aqt import mw
from aqt.qt import *
from .format_and_edit import *

class ConfigUI(QDialog):
    def __init__(self, addon_parent):
        super(ConfigUI, self).__init__(addon_parent)
        
        self.addon_parent = addon_parent
        self.config = self.addon_parent.addonManager.getConfig(__name__)

        self.setWindowTitle("Config")

        # Whole layout & categorical layouts
        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.general_tab = QWidget()
        self.words_tab = QWidget()

        ### general tab ###
        self.general_layout = QVBoxLayout()
        self.box1 = QGroupBox("(1) Show 'Format / Edit'")
        self.box2 = QGroupBox("(2) Quick Access Items")
        self.boxPos = QGroupBox("(3) Quick Access Position")
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layoutPos = QHBoxLayout()
        self.boxB = QGroupBox("Text Styling")
        self.boxC = QGroupBox("Text Color")
        self.boxD = QGroupBox("Font Size")
        self.boxE = QGroupBox("Alignment / List")
        self.boxF = QGroupBox("Date / Time")
        self.boxG = QGroupBox("(Clear Format)")

            # (A)Show in Editor/Reviewer
        self.layoutA = QVBoxLayout()

                ## Editor checkbox
        self.editor_checkbox = QCheckBox("Show 'Format / Edit' in Editor context menu")
        self.editor_checkbox.setChecked(self.config.get('editor', {}).get('enabled', True))
        self.layoutA.addWidget(self.editor_checkbox)

                ## Reviewer checkbox
        self.reviewer_checkbox = QCheckBox("Show 'Format / Edit' in Reviewer context menu")
        self.reviewer_checkbox.setChecked(self.config.get('reviewer', {}).get('enabled', True))
        self.layoutA.addWidget(self.reviewer_checkbox)

            # (B)text_styling_actions
        self.layoutB = QVBoxLayout()

                ## text_styling_actions_checkboxes
        self.text_styling_actions_checkboxes = []
        for action_name, command, value in text_styling_actions:
            checkbox = QCheckBox(action_name)
            checkbox.setChecked(action_name in self.config.get('selected_quick_access_items', []))
            self.layoutB.addWidget(checkbox)
            self.text_styling_actions_checkboxes.append(checkbox)
        self.layoutB.addStretch(1)

            # (C)text_color_actions
        self.layoutC = QVBoxLayout()

                ## text_color_actions_checkboxes
        self.text_color_actions_checkboxes = []
        for action_name, command, value in text_color_actions:
            checkbox = QCheckBox(action_name)
            checkbox.setChecked(action_name in self.config.get('selected_quick_access_items', []))
            self.layoutC.addWidget(checkbox)
            self.text_color_actions_checkboxes.append(checkbox)
        self.layoutC.addStretch(1)

            # (D)font_size_actions
        self.layoutD = QVBoxLayout()

                ## font_size_actions_checkboxes
        self.font_size_actions_checkboxes = []
        for action_name, command, value in font_size_actions:
            checkbox = QCheckBox(action_name)
            checkbox.setChecked(action_name in self.config.get('selected_quick_access_items', []))
            self.layoutD.addWidget(checkbox)
            self.font_size_actions_checkboxes.append(checkbox)
        self.layoutD.addStretch(1)

            # (E)alignment_actions
        self.layoutE = QVBoxLayout()

                ## font_size_actions_checkboxes
        self.alignment_actions_checkboxes = []
        for action_name, command, value in alignment_actions:
            checkbox = QCheckBox(action_name)
            checkbox.setChecked(action_name in self.config.get('selected_quick_access_items', []))
            self.layoutE.addWidget(checkbox)
            self.alignment_actions_checkboxes.append(checkbox)
        self.layoutE.addStretch(1)

            # (F)date_and_time_formats
        self.layoutF = QVBoxLayout()

                ## date_and_time_formats_checkboxes
        self.date_and_time_formats_checkboxes = []
        for action_name, command, value in date_and_time_formats:
            checkbox = QCheckBox(action_name)
            checkbox.setChecked(action_name in self.config.get('selected_quick_access_items', []))
            self.layoutF.addWidget(checkbox)
            self.date_and_time_formats_checkboxes.append(checkbox)
        self.layoutF.addStretch(1)

            # (G)clear_format
        self.layoutG = QVBoxLayout()

                ## date_and_time_format_checkboxes
        self.clear_format_checkboxes = []
        for action_name, command, value in clear_format:
            checkbox = QCheckBox(action_name)
            checkbox.setChecked(action_name in self.config.get('selected_quick_access_items', []))
            self.layoutG.addWidget(checkbox)
            self.clear_format_checkboxes.append(checkbox)
        self.layoutG.addStretch(1)

            ## Quick Access position
        self.quick_access_position_checkbox = QCheckBox("Display the Quick Access items on the first level of the context menu")
        self.quick_access_position_checkbox.setChecked(self.config.get('quick_access_position', False))
        self.layoutPos.addWidget(self.quick_access_position_checkbox)

        ### special characters tab ###
        self.words_layout = QVBoxLayout()

            ## user words checkbox
        self.words_checkbox = QCheckBox("Show 'User Words' (the added words below) in the context menu")
        self.words_checkbox.setChecked(self.config.get('user_words_flag', True))
        self.words_layout.addWidget(self.words_checkbox)

            ## Add, edit and remove buttons
        self.add_button_layout = QHBoxLayout()
        self.add_words_button = QPushButton("Add")
        self.add_words_button.clicked.connect(self.add_word)
        self.edit_remove_buttons_layout = QHBoxLayout()
        self.edit_words_button = QPushButton("Edit")
        self.edit_words_button.clicked.connect(self.edit_word)
        self.remove_words_button = QPushButton("Remove")
        self.remove_words_button.clicked.connect(self.remove_word)

        self.add_button_layout.addWidget(self.add_words_button)
        self.edit_remove_buttons_layout.addWidget(self.edit_words_button)
        self.edit_remove_buttons_layout.addWidget(self.remove_words_button)
        self.words_layout.addLayout(self.add_button_layout)
        self.words_layout.addLayout(self.edit_remove_buttons_layout)

            ## user words list
        self.words_list_widget = QListWidget()
        for char in self.config.get('user_words', []):
            self.words_list_widget.addItem(char)
        self.words_layout.addWidget(self.words_list_widget)

            ## Up and down buttons
        self.updownbuttons_layout = QHBoxLayout()
        self.up_button = QPushButton("Move Up")
        self.up_button.clicked.connect(self.move_up)
        self.down_button = QPushButton("Move Down")
        self.down_button.clicked.connect(self.move_down)

        self.updownbuttons_layout.addWidget(self.up_button)
        self.updownbuttons_layout.addWidget(self.down_button)
        self.words_layout.addLayout(self.updownbuttons_layout)

            ## Import and export buttons
        self.import_export_buttons_layout = QHBoxLayout()
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.import_words)
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_words)

        self.import_export_buttons_layout.addWidget(self.import_button)
        self.import_export_buttons_layout.addWidget(self.export_button)
        self.words_layout.addLayout(self.import_export_buttons_layout)

            ## Quick Access position
        self.words_position_checkbox = QCheckBox("Display the added words on the first level of the context menu")
        self.words_position_checkbox.setChecked(self.config.get('user_words_position', False))
        self.words_layout.addWidget(self.words_position_checkbox)

        self.words_tab.setLayout(self.words_layout)

        ### OK and Cancel buttons ###
        self.layoutOKCancel = QHBoxLayout()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_config)
        self.button_box.rejected.connect(self.reject)

        # Combine the layouts
        self.layout1.addLayout(self.layoutA)

        self.boxB.setLayout(self.layoutB)
        self.boxC.setLayout(self.layoutC)
        self.boxD.setLayout(self.layoutD)
        self.boxE.setLayout(self.layoutE)
        self.boxF.setLayout(self.layoutF)
        self.boxG.setLayout(self.layoutG)
        self.layout2.addWidget(self.boxB)
        self.layout2.addWidget(self.boxC)
        self.layout2.addWidget(self.boxD)
        self.layout2.addWidget(self.boxE)
        self.layout2.addWidget(self.boxF)
        self.layout2.addWidget(self.boxG)

        self.box1.setLayout(self.layout1)
        self.box2.setLayout(self.layout2)
        self.boxPos.setLayout(self.layoutPos)

        self.general_layout.addWidget(self.box1)
        self.general_layout.addWidget(self.box2)
        self.general_layout.addWidget(self.boxPos)

        self.general_tab.setLayout(self.general_layout)
        self.words_tab.setLayout(self.words_layout)

        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.words_tab, "User Words")

        self.layoutOKCancel.addWidget(self.button_box)

        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.layoutOKCancel)
        self.setLayout(self.layout)

        # Merge all the checkboxes lists
        self.quick_access_checkboxes = self.text_styling_actions_checkboxes + self.text_color_actions_checkboxes + self.font_size_actions_checkboxes + self.alignment_actions_checkboxes + self.date_and_time_formats_checkboxes

    # Function to add a word
    def add_word(self):
        text, ok = QInputDialog.getText(self, 'Add word', 'Enter the word:')
        if ok and text:
            self.words_list_widget.addItem(text)

    # Function to edit a word
    def edit_word(self):
        current_row = self.words_list_widget.currentRow()
        item = self.words_list_widget.item(current_row)
        if item:
            old_text = item.text()
            new_text, ok = QInputDialog.getText(self, "Edit Word", "New Word:", QLineEdit.Normal, old_text)
            if ok and new_text != old_text:
                item.setText(new_text)

    # Function to remove a word
    def remove_word(self):
        current_item = self.words_list_widget.currentItem()
        if current_item:
            self.words_list_widget.takeItem(self.words_list_widget.row(current_item))

    # Function to move selected item up
    def move_up(self):
        current_row = self.words_list_widget.currentRow()
        if current_row > 0:
            item = self.words_list_widget.takeItem(current_row)
            self.words_list_widget.insertItem(current_row - 1, item)
            self.words_list_widget.setCurrentRow(current_row - 1)

    # Function to move selected item down
    def move_down(self):
        current_row = self.words_list_widget.currentRow()
        if current_row < self.words_list_widget.count() - 1:
            item = self.words_list_widget.takeItem(current_row)
            self.words_list_widget.insertItem(current_row + 1, item)
            self.words_list_widget.setCurrentRow(current_row + 1)

    # Function to import words from a file
    def import_words(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    words = file.read().strip().splitlines()
                    self.words_list_widget.clear()
                    self.words_list_widget.addItems(words)
                QMessageBox.information(self, "Information", "Successfully imported.")
            except Exception as e:
                QMessageBox.critical(self, "Error", "Failed to import words: " + str(e) + "\n\nPlease not that the file needs to have a line break after each word.")

    # Function to export words to a file
    def export_words(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    words = [self.words_list_widget.item(i).text() for i in range(self.words_list_widget.count())]
                    file.write('\n'.join(words))
                QMessageBox.information(self, "Information", "Successfully exported.")
            except Exception as e:
                QMessageBox.critical(self, "Error", "Failed to export words: " + str(e))

    # Function to save the configration
    def save_config(self):
        self.config['editor']['enabled'] = self.editor_checkbox.isChecked()
        self.config['reviewer']['enabled'] = self.reviewer_checkbox.isChecked()
        self.config['selected_quick_access_items'] = [checkbox.text() for checkbox in self.quick_access_checkboxes if checkbox.isChecked()]
        self.config['quick_access_position'] = self.quick_access_position_checkbox.isChecked()
        self.config['user_words_flag'] = self.words_checkbox.isChecked()
        self.config['user_words'] = [self.words_list_widget.item(i).text() for i in range(self.words_list_widget.count())]
        self.config['user_words_position'] = self.words_position_checkbox.isChecked()
        self.addon_parent.addonManager.writeConfig(__name__, self.config)
        self.accept()

def open_config_dialog():
    dialog = ConfigUI(mw)
    dialog.exec_()

mw.addonManager.setConfigAction(__name__, open_config_dialog)
