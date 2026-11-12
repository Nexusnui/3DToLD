import platform
from tomlkit import TOMLDocument
from ThreeDToLD import __version__
from ThreeDToLD.config import config_path
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPlainTextEdit,
)


class AboutPage(QDialog):
    def __init__(self, config: TOMLDocument, parent= None):
        super().__init__(parent)
        self.setWindowTitle("About 3DToLD")
        main_layout = QVBoxLayout()
        # Todo: Install Method
        self.info_widget: QPlainTextEdit = QPlainTextEdit(
            f"3DToLD Version: {__version__}\n"
            f"Python Version: {platform.python_version()}\n"
            f"Platform: {platform.platform()}\n"
            f"Config Path: \n'{config_path}'\n")
        self.info_widget.setReadOnly(True)
        main_layout.addWidget(self.info_widget)
        self.setLayout(main_layout)