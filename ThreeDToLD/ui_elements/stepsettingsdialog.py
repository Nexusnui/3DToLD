from PyQt6.QtWidgets import (
    QHBoxLayout,
    QApplication,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QCheckBox,
    QPushButton,
    QLabel
)


class StepSettingsDialog(QDialog):

    def __init__(self, parent=None,
                 tol_linear: int | float = None,
                 tol_angular: int | float = None,
                 tol_relative: bool = False):
        super().__init__(parent)
        self.setWindowTitle("Step File Quality Settings")
        if tol_linear is None:
            self.tol_linear = 0.1
        else:
            self.tol_linear = tol_linear
        if tol_angular is None:
            self.tol_angular = 0.5
        else:
            self.tol_angular = tol_angular
        self.tol_relative = tol_relative

        main_layout = QVBoxLayout()

        description_label = QLabel("Parameters used by Cascadio for meshing Step files.")
        main_layout.addWidget(description_label)

        input_layout = QFormLayout()

        self.tol_linear_input = QDoubleSpinBox()
        self.tol_linear_input.valueChanged.connect(self.linear_changed)
        self.tol_linear_input.setDecimals(3)
        self.tol_linear_input.setValue(self.tol_linear)

        tol_linear_label = QLabel("Tolerance Linear ℹ️")
        tol_linear_label.setToolTip("How large should angular deflection be allowed.\n"
                                    "Uses model units.\n"
                                    "0.01 is the used by Cascadio.")
        input_layout.addRow(tol_linear_label, self.tol_linear_input)

        self.tol_angular_input = QDoubleSpinBox()
        self.tol_angular_input.valueChanged.connect(self.angle_changed)
        self.tol_angular_input.setDecimals(3)
        self.tol_angular_input.setValue(self.tol_angular)

        tol_angular_label = QLabel("Tolerance Angular ℹ️")
        tol_angular_label.setToolTip("How large should linear deflection be allowed.")
        input_layout.addRow(tol_angular_label, self.tol_angular_input)

        self.tol_relative_check = QCheckBox()
        self.tol_relative_check.setChecked(self.tol_relative)
        self.tol_relative_check.checkStateChanged.connect(self.merge_check_changed)

        tol_relative_label = QLabel("Tolerance Relative ℹ️")
        tol_relative_label.setToolTip("Is tol_linear relative to edge length, or an absolute distance?")
        input_layout.addRow(tol_relative_label, self.tol_relative_check)

        reset_button = QPushButton("Reset Values")
        reset_button.clicked.connect(self.reset_values)
        input_layout.addRow(reset_button)

        main_layout.addLayout(input_layout)

        bottom_layout = QHBoxLayout()
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        bottom_layout.addWidget(button_box)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def angle_changed(self, angle):
        self.tol_angular = angle

    def linear_changed(self, length):
        self.tol_linear = length

    def merge_check_changed(self, check):
        self.tol_relative = not self.tol_relative

    def reset_values(self):
        self.tol_linear = 0.1
        self.tol_angular = 0.5
        self.tol_linear_input.setValue(self.tol_linear)
        self.tol_angular_input .setValue(self.tol_angular)
        self.tol_relative_check.setChecked(False)
        self.tol_relative = False


if __name__ == "__main__":
    app = QApplication([])

    line_dia = StepSettingsDialog()
    line_dia.exec()

    print(f"{line_dia.tol_linear=}\n"
          f"{line_dia.tol_angular=}\n"
          f"{line_dia.tol_relative}\n")
