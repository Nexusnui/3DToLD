from importlib import resources
import platform
from tomlkit import TOMLDocument
from ThreeDToLD import __version__
from ThreeDToLD.config import config_path
from ThreeDToLD.brick_data.brick_resources import get_update_date, user_brick_resources_filepath
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPlainTextEdit,
    QLayout
)


class AboutPage(QDialog):
    def __init__(self, config: TOMLDocument, parent= None):
        super().__init__(parent)
        self.setWindowTitle("About 3DToLD")
        main_layout = QVBoxLayout()

        install_path = __file__.split('ui_elements')[0]

        install_info = resources.read_text("ThreeDToLD", "install_info")
        self.info_widget: QPlainTextEdit = QPlainTextEdit(
            f"3DToLD Version: {__version__}\n"
            f"Brick Resources Updated on: {get_update_date()}\n"
            f"Installation Method: {install_info}\n"
            f"Python Version: {platform.python_version()}\n"
            f"Platform: {platform.platform()}\n"
            f"Installation Path:\n'{install_path}'\n"
            f"Config Path:\n'{config_path}'\n"
            f"Path to user updated Brick Resources:\n'{user_brick_resources_filepath}'\n"
        )
        self.info_widget.setReadOnly(True)
        font_size = self.info_widget.fontMetrics().lineSpacing()
        self.info_widget.setFixedHeight(font_size*13)
        self.info_widget.setMinimumWidth(font_size * 30)
        main_layout.addWidget(self.info_widget)
        self.setLayout(main_layout)
        main_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)