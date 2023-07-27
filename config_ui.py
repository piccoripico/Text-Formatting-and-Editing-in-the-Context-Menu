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
        self.box1 = QGroupBox("(1) Show 'Format / Edit'")
        self.box2 = QGroupBox("(2) Quick Access Items")
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
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

        # OK and Cancel buttons
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

        self.layout3.addWidget(self.button_box)

        self.box1.setLayout(self.layout1)
        self.box2.setLayout(self.layout2)

        self.layout.addWidget(self.box1)
        self.layout.addWidget(self.box2)
        self.layout.addLayout(self.layout3)

        self.setLayout(self.layout)

        # Merge all the checkboxes lists
        self.quick_access_checkboxes = self.text_styling_actions_checkboxes + self.text_color_actions_checkboxes + self.font_size_actions_checkboxes + self.alignment_actions_checkboxes + self.date_and_time_formats_checkboxes

    def save_config(self):
        self.config['editor']['enabled'] = self.editor_checkbox.isChecked()
        self.config['reviewer']['enabled'] = self.reviewer_checkbox.isChecked()
        self.config['selected_quick_access_items'] = [checkbox.text() for checkbox in self.quick_access_checkboxes if checkbox.isChecked()]
        self.addon_parent.addonManager.writeConfig(__name__, self.config)
        self.accept()

def open_config_dialog():
    dialog = ConfigUI(mw)
    dialog.exec_()

mw.addonManager.setConfigAction(__name__, open_config_dialog)
