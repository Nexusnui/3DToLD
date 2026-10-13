from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QTabWidget,
    QVBoxLayout,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QComboBox,
    QCheckBox,
    QDoubleSpinBox,
    QFileDialog,
    QMessageBox
)

from ThreeDToLD.brick_data.ldrawObject import LDrawConversionFactor, UpAxis, default_part_licenses
from ThreeDToLD.config import loadconfig, save_config, config_path
from ThreeDToLD.ui_elements.brickcolourwidget import ColourCategoriesDialog


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_changed = False
        self.config, warnings = loadconfig()
        if len(warnings) > 0:
            QMessageBox.critical(self, "Failed to load config", f"An Issue occurred during while loading the config:\n"
                                                                f"Following warning where returned:\n"
                                                                f"{warnings}")

        self.has_unsaved_changes = False

        main_layout = QVBoxLayout()
        self.category_tabs = QTabWidget()

        main_layout.addWidget(self.category_tabs)

        # First Tab: Paths + Theme
        first_tab = QWidget()
        first_tab_layout = QVBoxLayout()
        first_tab.setLayout(first_tab_layout)

        # Paths Area
        paths_area = QGroupBox("Paths")
        paths_layout = QVBoxLayout()
        paths_area.setLayout(paths_layout)

        model_path_label = QLabel("Model Path ℹ️")
        model_path_label.setToolTip("Initial path opened when selecting a 3d model.")

        paths_layout.addWidget(model_path_label)

        model_path_inputs = QHBoxLayout()
        self.model_path_line = QLineEdit()
        self.model_path_line.setReadOnly(True)
        self.model_path_line.setPlaceholderText("Select Working Directory")
        model_path_inputs.addWidget(self.model_path_line)

        self.select_model_path_button = QPushButton("Select")
        model_path_inputs.addWidget(self.select_model_path_button)
        self.select_model_path_button.clicked.connect(self.select_model_path)

        paths_layout.addLayout(model_path_inputs)

        first_tab_layout.addWidget(paths_area)

        # Theme Area
        theme_area = QGroupBox("Theme")
        theme_layout = QFormLayout()
        theme_area.setLayout(theme_layout)
        self.mode_input = QComboBox()
        self.mode_input.addItems(["System", "Dark", "Light"])
        self.mode_input.currentTextChanged.connect(self.input_changed)
        mode_label = QLabel("Mode ℹ️❗")
        mode_label.setToolTip("Theme of the application. Requires restart of the application.\n"
                              "Not implemented Yet!")
        theme_layout.addRow(mode_label, self.mode_input)

        first_tab_layout.addWidget(theme_area)

        first_tab_layout.addStretch()
        reset_config_button = QPushButton("Reset Settings to default")
        reset_config_button.clicked.connect(self.reset_config)
        first_tab_layout.addWidget(reset_config_button)
        config_path_area = QHBoxLayout()
        config_path_area.addWidget(QLabel("Path to User Config:"))
        config_path_label = QLineEdit()
        config_path_label.setText(config_path)
        config_path_label.setReadOnly(True)
        config_path_area.addWidget(config_path_label)
        first_tab_layout.addLayout(config_path_area)

        self.category_tabs.addTab(first_tab, "General")

        # Second Tab: Import Settings
        second_tab = QWidget()
        second_tab_layout = QVBoxLayout()
        second_tab.setLayout(second_tab_layout)
        second_tab_layout.addWidget(QLabel("Here you can set the default import settings.\n"
                                           "These are used at the start of the application."))

        load_file_inputs = QFormLayout()
        # Enable Multicolour Check
        self.multicolour_check = QCheckBox()
        multicolour_label = QLabel("Multicolour ℹ️")
        multicolour_label.setToolTip("If deactivated all objects are single colour")
        self.multicolour_check.checkStateChanged.connect(self.input_changed)
        load_file_inputs.addRow(multicolour_label, self.multicolour_check)

        # Enable Multi Objects Check
        self.multi_object_check = QCheckBox()
        multi_object_label = QLabel("Multiple Objects ℹ️")
        multi_object_label.setToolTip("If deactivated all submodels will be merged\n"
                                      "With multicolour unique colours are applied before merging\n"
                                      "(If the the file does not define colours)")
        self.multi_object_check.checkStateChanged.connect(self.input_changed)
        load_file_inputs.addRow(multi_object_label, self.multi_object_check)

        # Unit Selection
        self.unit_input = QComboBox()
        self.unit_input.addItems(LDrawConversionFactor.get_membernames_as_string())
        self.unit_input.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        category_label = QLabel("Unit ℹ️")
        category_label.setToolTip("Unit conversion used to convert to LDraw Units.\n"
                                  "If LDraw is selected no conversion is applied.\n"
                                  "If no Unit is found Millimeter is used by default.")
        self.unit_input.currentTextChanged.connect(self.input_changed)
        load_file_inputs.addRow(category_label, self.unit_input)

        # Set Scale
        self.scale_input = QDoubleSpinBox()
        self.scale_input.setValue(1.0)
        self.scale_input.setMaximum(999.999)
        self.scale_input.setMinimum(0.001)
        self.scale_input.setDecimals(3)
        scale_label = QLabel("Scale ℹ️")
        scale_label.setToolTip("Factor used to scale the model")
        self.scale_input.valueChanged.connect(self.input_changed)
        load_file_inputs.addRow(scale_label, self.scale_input)

        # Choose Up Axis
        self.orientation_input = QComboBox()
        self.orientation_input.addItems(UpAxis.get_membernames_as_string())
        ldraw_rotation_label = QLabel("Up Axis ℹ️")
        ldraw_rotation_label.setToolTip("Choose what the up axis of the model is.\n"
                                        "If '-Y' is chosen no rotation is applied.\n"
                                        "(In LDraws coordinate system -Y is up)")
        self.orientation_input.currentTextChanged.connect(self.input_changed)
        load_file_inputs.addRow(ldraw_rotation_label, self.orientation_input)

        # Use 3mf Loader Check
        self.threemfloader_check = QCheckBox()
        threemfloader_label = QLabel("Custom 3mf Loader ℹ️")
        threemfloader_label.setToolTip("Enables color support for 3mf files.\n"
                                       "MMU painting (Slic3r/Prusa/Bambu) not supported.\n"
                                       "Trimesh is used to load 3mf files when unchecked.")
        load_file_inputs.addRow(threemfloader_label, self.threemfloader_check)
        self.threemfloader_check.checkStateChanged.connect(self.input_changed)

        second_tab_layout.addLayout(load_file_inputs)

        step_quality_area = QGroupBox("Step Mesh Quality")
        step_quality_layout = QFormLayout()
        step_quality_area.setLayout(step_quality_layout)

        self.tol_linear_input = QDoubleSpinBox()
        self.tol_linear_input.setDecimals(3)
        tol_linear_label = QLabel("Tolerance Linear ℹ️")
        tol_linear_label.setToolTip("How large should angular deflection be allowed.\n"
                                    "Uses model units.\n"
                                    "0.01 is the used by Cascadio.")
        self.tol_linear_input.valueChanged.connect(self.input_changed)
        step_quality_layout.addRow(tol_linear_label, self.tol_linear_input)

        self.tol_angular_input = QDoubleSpinBox()
        self.tol_angular_input.setDecimals(3)
        tol_angular_label = QLabel("Tolerance Angular ℹ️")
        tol_angular_label.setToolTip("How large should linear deflection be allowed.")
        self.tol_angular_input.valueChanged.connect(self.input_changed)
        step_quality_layout.addRow(tol_angular_label, self.tol_angular_input)

        self.tol_relative_check = QCheckBox()
        tol_relative_label = QLabel("Tolerance Relative ℹ️")
        tol_relative_label.setToolTip("Is tol_linear relative to edge length, or an absolute distance?")
        self.tol_relative_check.checkStateChanged.connect(self.input_changed)
        step_quality_layout.addRow(tol_relative_label, self.tol_relative_check)

        second_tab_layout.addWidget(step_quality_area)

        self.category_tabs.addTab(second_tab, "Import Settings")

        # Third Tab: Metadata
        third_tab = QWidget()
        third_tab_layout = QFormLayout()
        third_tab.setLayout(third_tab_layout)
        third_tab_layout.addRow(QLabel("Here you can set the default Metadata settings.\n"
                                       "Some of these are used at the start of the application."))

        self.name_from_metadata_check = QCheckBox()
        name_from_metadata_label = QLabel("Part Name from Metadata ℹ️")
        name_from_metadata_label.setToolTip("Use name from metadata, if non existend or set to false use filename")
        self.name_from_metadata_check.checkStateChanged.connect(self.input_changed)
        third_tab_layout.addRow(name_from_metadata_label, self.name_from_metadata_check)

        self.default_author_line = QLineEdit()
        self.default_author_line.setPlaceholderText("Your Name/Alias")
        default_author_label = QLabel("Default Author ℹ️")
        default_author_label.setToolTip("'Realname[LDraw username]'\n"
                                        "Is used for official LDraw files\n")
        self.default_author_line.textChanged.connect(self.input_changed)
        third_tab_layout.addRow(default_author_label, self.default_author_line)

        self.author_from_metadata_check = QCheckBox()
        author_from_metadata_label = QLabel("Use Author from Metadata ℹ️")
        author_from_metadata_label.setToolTip("If true the default author is replaced, "
                                              "if another is found in the Metadata.")
        self.author_from_metadata_check.checkStateChanged.connect(self.input_changed)
        third_tab_layout.addRow(author_from_metadata_label, self.author_from_metadata_check)

        self.default_part_license_input = QComboBox()
        self.default_part_license_input.addItems(default_part_licenses)
        self.default_part_license_input.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.default_part_license_input.setEditable(True)
        default_part_license_label = QLabel("Part License (Optional) ℹ️")
        default_part_license_label.setToolTip("License of the Part, set your own one or use one from the list.")
        self.default_part_license_input.currentTextChanged.connect(self.input_changed)
        third_tab_layout.addRow(default_part_license_label, self.default_part_license_input)

        self.license_from_metadata_check = QCheckBox()
        license_from_metadata_label = QLabel("Use License from Metadata ℹ️")
        license_from_metadata_label.setToolTip("Default license is replaced if another is found in the Metadata.")
        self.license_from_metadata_check.checkStateChanged.connect(self.input_changed)
        third_tab_layout.addRow(license_from_metadata_label, self.license_from_metadata_check)

        self.category_tabs.addTab(third_tab, "Metadata")

        # Fourth Tab: Other
        fourth_tab = QWidget()
        fourth_tab_layout = QFormLayout()
        fourth_tab.setLayout(fourth_tab_layout)

        default_colour_categories_label = QLabel("Default Colour Categories for Conversion ℹ️")
        default_colour_categories_button = QPushButton("Select")
        default_colour_categories_button.clicked.connect(self.select_colour_categories)
        default_colour_categories_label.setToolTip("List of Colour Categories used for Conversion of LDraw Colours.")
        fourth_tab_layout.addRow(default_colour_categories_label, default_colour_categories_button)

        self.convert_colours_on_load_check = QCheckBox()
        convert_colours_on_load_label = QLabel("Convert to LDraw Colours on Load ℹ️❗")
        convert_colours_on_load_label.setToolTip("Use default colour categories to convert colours on file import.\n"
                                                 "Not implemented Yet!")

        self.convert_colours_on_load_check.checkStateChanged.connect(self.input_changed)
        fourth_tab_layout.addRow(convert_colours_on_load_label, self.convert_colours_on_load_check)

        self.category_tabs.addTab(fourth_tab, "Other")

        dialog_inputs = QHBoxLayout()
        dialog_inputs.addStretch()
        self.save_button = QPushButton("Save")
        close_button = QPushButton("Close")

        self.save_button.clicked.connect(self.save_config)
        close_button.clicked.connect(self.reject)
        dialog_inputs.addWidget(self.save_button)
        dialog_inputs.addWidget(close_button)
        main_layout.addLayout(dialog_inputs)

        self.set_input_values()
        self.save_button.setDisabled(True)
        self.has_unsaved_changes = False
        self.setWindowTitle("Settings")

        self.setLayout(main_layout)

    def save_config(self):
        # Values First Tab
        self.config["Theme"]["mode"] = self.mode_input.currentText()
        # Values Second Tab
        self.config["Import_Settings"]["multicolour"] = self.multicolour_check.isChecked()
        self.config["Import_Settings"]["multiple_objects"] = self.multi_object_check.isChecked()
        self.config["Import_Settings"]["unit"] = self.unit_input.currentText()
        self.config["Import_Settings"]["scale"] = self.scale_input.value()
        self.config["Import_Settings"]["up_axis"] = self.orientation_input.currentText()
        self.config["Import_Settings"]["custom_3mf_loader"] = self.threemfloader_check.isChecked()
        self.config["Import_Settings"]["Step_Settings"]["tol_linear"] = self.tol_linear_input.value()
        self.config["Import_Settings"]["Step_Settings"]["tol_angular"] = self.tol_angular_input.value()
        self.config["Import_Settings"]["Step_Settings"]["tol_relative"] = self.tol_relative_check.isChecked()
        # Values Third Tab
        self.config["Metadata"]["name_from_metadata"] = self.name_from_metadata_check.isChecked()
        self.config["Metadata"]["default_author"] = self.default_author_line.text()
        self.config["Metadata"]["author_from_metadata"] = self.author_from_metadata_check.isChecked()
        self.config["Metadata"]["default_license"] = self.default_part_license_input.currentText()
        self.config["Metadata"]["license_from_metadata"] = self.license_from_metadata_check.isChecked()
        # Values Fourth Tab
        self.config["Convert_To_LDraw_Colours"][
            "convert_colours_on_load"] = self.convert_colours_on_load_check.isChecked()

        if not save_config(self.config):
            QMessageBox.critical(self, "Failed to save settings", f"Failed to save settings in config file:\n"
                                                                  f"{config_path}")
        else:
            self.save_button.setDisabled(True)
            self.has_unsaved_changes = False
            self.config_changed = True
            self.setWindowTitle("Settings")

    def reject(self):
        if self.has_unsaved_changes:
            answer = QMessageBox.question(
                self,
                "Close Settings?",
                "There might be unsaved settings!\n Close anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if answer == QMessageBox.StandardButton.Yes:
                super().reject()
        else:
            super().reject()

    def reset_config(self):
        answer = QMessageBox.question(
            self,
            "Reset Settings?",
            "Reset all Settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.config, warnings = loadconfig(True)
            if len(warnings) < 1:
                self.set_input_values()
                self.has_unsaved_changes = False
                self.save_button.setDisabled(True)
            else:
                QMessageBox.critical(self, "Failed to Reset", f"Failed to reset settings.\n"
                                                              f"The folliwing warnings were returned:\n"
                                                              f"{warnings}")

    def select_model_path(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        if dialog.exec():
            filepath = dialog.selectedFiles()[0]
            self.input_changed()
            self.model_path_line.setText(filepath)
            self.config["Paths"]["model_path"] = filepath

    def set_input_values(self):
        # Values First Tab
        self.model_path_line.setText(self.config["Paths"]["model_path"])
        self.mode_input.setCurrentText(self.config["Theme"]["mode"])
        # Values Second Tab
        self.multicolour_check.setChecked(self.config["Import_Settings"]["multicolour"])
        self.multi_object_check.setChecked(self.config["Import_Settings"]["multiple_objects"])
        self.unit_input.setCurrentText(self.config["Import_Settings"]["unit"])
        self.scale_input.setValue(self.config["Import_Settings"]["scale"])
        self.orientation_input.setCurrentText(self.config["Import_Settings"]["up_axis"])
        self.threemfloader_check.setChecked(self.config["Import_Settings"]["custom_3mf_loader"])
        self.tol_linear_input.setValue(self.config["Import_Settings"]["Step_Settings"]["tol_linear"])
        self.tol_angular_input.setValue(self.config["Import_Settings"]["Step_Settings"]["tol_angular"])
        self.tol_relative_check.setChecked(self.config["Import_Settings"]["Step_Settings"]["tol_relative"])
        # Values Third Tab
        self.name_from_metadata_check.setChecked(self.config["Metadata"]["name_from_metadata"])
        self.default_author_line.setText(self.config["Metadata"]["default_author"])
        self.author_from_metadata_check.setChecked(self.config["Metadata"]["author_from_metadata"])
        self.default_part_license_input.setCurrentText(self.config["Metadata"]["default_license"])
        self.license_from_metadata_check.setChecked(self.config["Metadata"]["license_from_metadata"])
        # Values Fourth Tab
        self.convert_colours_on_load_check.setChecked(
            self.config["Convert_To_LDraw_Colours"]["convert_colours_on_load"])

    def select_colour_categories(self):
        categories_dialog = ColourCategoriesDialog(
            message="Select Colour Categories used by default for colour conversion.",
            checked_categories=self.config["Convert_To_LDraw_Colours"]["default_colour_categories"]
        )
        if categories_dialog.exec():
            colour_categories = categories_dialog.get_selected_items()
            self.config["Convert_To_LDraw_Colours"]["default_colour_categories"] = colour_categories
            self.input_changed()

    def input_changed(self):
        self.has_unsaved_changes = True
        self.save_button.setEnabled(True)
        self.setWindowTitle("Settings*")


if __name__ == "__main__":
    app = QApplication([])

    settings_dia = SettingsDialog()
    settings_dia.exec()
