from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QPushButton,
    QLayout,
    QLabel,
    QProgressDialog,
    QMessageBox
)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from ThreeDToLD.brick_data.brick_resources import update_brick_resources, get_update_date
from ThreeDToLD import __version__


def open_link():
    QDesktopServices.openUrl(QUrl("https://github.com/Nexusnui/3DToLD/releases/latest"))


class UpdateDialog(QDialog):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setWindowTitle("Updates for 3DToLD")
        main_layout = QFormLayout()
        main_layout.addRow("3DToLD Version:", QLabel(__version__))
        link_label = QPushButton("View Latest Release")
        link_label.clicked.connect(open_link)
        main_layout.addRow("Update 3DToLD", link_label)
        self.brick_resources_update_label = QLabel(str(get_update_date()))
        main_layout.addRow("Brick Resources Updated on:", self.brick_resources_update_label)
        update_brick_resources_label = QLabel("Update Brick Resources\nfrom LDraw.org ℹ️")
        update_brick_resources_label.setToolTip("Brick Resources include:\n"
                                                "- Brick Categories\n"
                                                "- Colours\n"
                                                "- Colour Categories")
        update_brick_resources_button = QPushButton("Update Brick Resources")
        update_brick_resources_button.clicked.connect(self.update_brick_resources)
        main_layout.addRow(update_brick_resources_label, update_brick_resources_button)

        self.setLayout(main_layout)
        main_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)


    def update_brick_resources(self):
        progress_dialog = UpdateProgressDialog(self)
        last_msg = ""
        progress_dialog.setValue(1)
        progress_values = [10,60,80,90,101]
        progress_dialog.show()
        for progress, msg in enumerate(update_brick_resources()):
            last_msg = msg
            progress_dialog.setLabelText(last_msg)
            progress_dialog.setValue(progress_values[progress])
        progress_dialog.manually_close()
        self.brick_resources_update_label.setText(str(get_update_date()))
        QMessageBox.information(self,"Update Result", f"Update finished with the following message:\n{last_msg}")


class UpdateProgressDialog(QProgressDialog):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setWindowTitle("Update Brick Resources")
        self.setCancelButton(None)
        self.setModal(True)

    def reject(self):
        ...

    def closeEvent(self, event):
        if event.spontaneous():
            event.ignore()

    def manually_close(self):
        super().close()