from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QPushButton
)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl


def open_link():
    QDesktopServices.openUrl(QUrl("https://github.com/Nexusnui/3DToLD/releases/latest"))


class UpdateDialog(QDialog):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setWindowTitle("About 3DToLD")
        main_layout = QFormLayout()
        link_label = QPushButton("View Latest Release")
        link_label.clicked.connect(open_link)
        main_layout.addRow("Update 3DToLD", link_label)

        self.setLayout(main_layout)
