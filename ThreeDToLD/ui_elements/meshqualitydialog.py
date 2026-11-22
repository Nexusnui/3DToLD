from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QCheckBox,
    QPushButton,
    QLabel,
    QTabWidget,
    QWidget,
    QSpinBox,
    QLayout
)


class MeshQualityDialog(QDialog):

    def __init__(self, parent=None,
                 tol_linear: int | float = 0.1,
                 tol_angular: int | float = 0.5,
                 tol_relative: bool = False,
                 apply_mesh_simplification: bool = False,
                 use_percentage: bool = True,
                 simplification_percentage: float | int = 0.0,
                 simplification_face_count: int = 10000,
                 ):
        super().__init__(parent)
        self.setWindowTitle("Mesh Quality Settings")

        self.tol_linear: int | float = tol_linear
        self.tol_angular: int | float = tol_angular
        self.tol_relative: bool = tol_relative
        self.apply_mesh_simplification: bool = apply_mesh_simplification
        self.use_percentage: bool = use_percentage
        self.simplification_percentage: float | int = simplification_percentage
        self.simplification_face_count: int = simplification_face_count

        main_layout = QVBoxLayout()
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        mesh_tab = QWidget()
        mesh_layout = QVBoxLayout()
        mesh_tab.setLayout(mesh_layout)

        mesh_description_label = QLabel("Mesh Simplification Settings. If applied colours will be lost.")
        mesh_layout.addWidget(mesh_description_label)

        mesh_input_layout = QFormLayout()

        self.apply_mesh_simplification_check: QCheckBox = QCheckBox()
        self.apply_mesh_simplification_check.setChecked(self.apply_mesh_simplification)
        self.apply_mesh_simplification_check.checkStateChanged.connect(self.apply_simplification_changed)
        apply_mesh_simplification_label = QLabel("Apply Mesh Simplification")
        apply_mesh_simplification_label.setToolTip("Apply mesh simplification to all meshes.\n"
                                                   "Colour information will be lost.")
        mesh_input_layout.addRow(apply_mesh_simplification_label, self.apply_mesh_simplification_check)

        self.use_percentage_check: QCheckBox = QCheckBox()
        self.use_percentage_check.setChecked(self.use_percentage)
        self.use_percentage_check.checkStateChanged.connect(self.use_percentage_changed)
        use_percentage_label = QLabel("Use Percentage ℹ️")
        use_percentage_label.setToolTip("Use percentage for mesh simplification.\n"
                                        "If false face count is used.")
        mesh_input_layout.addRow(use_percentage_label, self.use_percentage_check)

        self.simplification_percentage_input: QDoubleSpinBox = QDoubleSpinBox()
        self.simplification_percentage_input.setDecimals(4)
        self.simplification_percentage_input.setMaximum(1)
        self.simplification_percentage_input.setMinimum(0.0001)
        self.simplification_percentage_input.setValue(simplification_percentage)
        self.simplification_percentage_input.setSingleStep(0.1)
        self.simplification_percentage_input.valueChanged.connect(self.percentage_changed)
        simplification_percentage_label: QLabel = QLabel("Percentage ℹ️")
        simplification_percentage_label.setToolTip("Amount by which all meshes is simplified.\n"
                                                   "For example 0.7 -> Reduces meshes by 70%")
        mesh_input_layout.addRow(simplification_percentage_label, self.simplification_percentage_input)

        self.simplification_face_count_input: QSpinBox = QSpinBox()
        self.simplification_face_count_input.setMinimum(1)
        self.simplification_face_count_input.setMaximum(16777215)
        self.simplification_face_count_input.setValue(simplification_face_count)
        self.simplification_face_count_input.valueChanged.connect(self.face_count_changed)
        simplification_face_count_label = QLabel("Face Count ℹ️")
        simplification_face_count_label.setToolTip("Minimum amount of faces meshes have after simplification.")
        mesh_input_layout.addRow(simplification_face_count_label, self.simplification_face_count_input)

        mesh_layout.addLayout(mesh_input_layout)
        tabs.addTab(mesh_tab, "Mesh Simplification")

        step_settings_tab = QWidget()
        step_settings_layout = QVBoxLayout()
        step_settings_tab.setLayout(step_settings_layout)

        step_description_label = QLabel("Parameters used by Cascadio for meshing Step files.")
        step_settings_layout.addWidget(step_description_label)

        step_input_layout = QFormLayout()

        self.tol_linear_input: QDoubleSpinBox = QDoubleSpinBox()
        self.tol_linear_input.valueChanged.connect(self.linear_changed)
        self.tol_linear_input.setDecimals(3)
        self.tol_linear_input.setValue(self.tol_linear)

        tol_linear_label: QLabel = QLabel("Tolerance Linear ℹ️")
        tol_linear_label.setToolTip("How large should angular deflection be allowed.\n"
                                    "Uses model units.\n"
                                    "0.01 is the used by Cascadio.")
        step_input_layout.addRow(tol_linear_label, self.tol_linear_input)

        self.tol_angular_input: QDoubleSpinBox = QDoubleSpinBox()
        self.tol_angular_input.valueChanged.connect(self.angle_changed)
        self.tol_angular_input.setDecimals(3)
        self.tol_angular_input.setValue(self.tol_angular)

        tol_angular_label: QLabel = QLabel("Tolerance Angular ℹ️")
        tol_angular_label.setToolTip("How large should linear deflection be allowed.")
        step_input_layout.addRow(tol_angular_label, self.tol_angular_input)

        self.tol_relative_check: QCheckBox = QCheckBox()
        self.tol_relative_check.setChecked(self.tol_relative)
        self.tol_relative_check.checkStateChanged.connect(self.merge_check_changed)

        tol_relative_label = QLabel("Tolerance Relative ℹ️")
        tol_relative_label.setToolTip("Is tol_linear relative to edge length, or an absolute distance?")
        step_input_layout.addRow(tol_relative_label, self.tol_relative_check)

        reset_button = QPushButton("Reset Values")
        reset_button.clicked.connect(self.reset_values)
        step_input_layout.addRow(reset_button)

        step_settings_layout.addLayout(step_input_layout)

        bottom_layout = QHBoxLayout()
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        bottom_layout.addWidget(button_box)

        main_layout.addLayout(bottom_layout)

        self.use_percentage_changed()
        self.apply_simplification_changed()

        tabs.addTab(step_settings_tab, "Step Meshing")
        self.setLayout(main_layout)
        main_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

    def apply_simplification_changed(self):
        self.apply_mesh_simplification = self.apply_mesh_simplification_check.isChecked()
        if self.apply_mesh_simplification_check.isChecked():
            self.use_percentage_check.setEnabled(True)
            if self.use_percentage_check.isChecked():
                self.simplification_percentage_input.setEnabled(True)
            else:
                self.simplification_face_count_input.setEnabled(True)
        else:
            self.use_percentage_check.setDisabled(True)
            if self.use_percentage_check.isChecked():
                self.simplification_percentage_input.setDisabled(True)
            else:
                self.simplification_face_count_input.setDisabled(True)

    def use_percentage_changed(self):
        self.use_percentage = self.use_percentage_check.isChecked()
        if self.use_percentage_check.isChecked():
            self.simplification_percentage_input.setEnabled(True)
            self.simplification_face_count_input.setDisabled(True)
        else:
            self.simplification_percentage_input.setDisabled(True)
            self.simplification_face_count_input.setEnabled(True)

    def percentage_changed(self):
        self.simplification_percentage = self.simplification_percentage_input.value()

    def face_count_changed(self):
        self.simplification_face_count = self.simplification_face_count_input.value()

    def angle_changed(self, angle):
        self.tol_angular = angle

    def linear_changed(self, length):
        self.tol_linear = length

    def merge_check_changed(self):
        self.tol_relative = not self.tol_relative

    def reset_values(self):
        self.tol_linear = 0.1
        self.tol_angular = 0.5
        self.tol_linear_input.setValue(self.tol_linear)
        self.tol_angular_input .setValue(self.tol_angular)
        self.tol_relative_check.setChecked(False)
        self.tol_relative = False
