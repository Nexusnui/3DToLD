import os
from collections import OrderedDict

import qdarktheme
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ThreeDToLD.config import loadconfig
from ThreeDToLD.brick_data.brickcolour import Brickcolour

from ThreeDToLD.ui_elements.aboutPage import AboutPage
from ThreeDToLD.ui_elements.brickcolourwidget import BrickcolourDialog, ColourCategoriesDialog, SplitColourDialog
from ThreeDToLD.ui_elements.exceptiondialog import ExceptionDialog
from ThreeDToLD.ui_elements.line_generation_dialog import LineGenerationDialog, LinePreset
from ThreeDToLD.ui_elements.settingsdialog import SettingsDialog
from ThreeDToLD.ui_elements.stepsettingsdialog import StepSettingsDialog


def about_page_test(test_config):
    about_page = AboutPage(test_config)
    about_page.exec()

def brick_colour_dialog_test():
    colour_dia = BrickcolourDialog()
    colour_dia.exec()

def color_category_dialog_test():
    colour_cat_dia = ColourCategoriesDialog()
    colour_cat_dia.exec()
    print(colour_cat_dia.get_selected_items())

def exception_dialog_test():
    exc_dia = ExceptionDialog(clipboard=app.clipboard())
    exc_dia.exec()

def line_generation_dialog_test():
    line_dia = LineGenerationDialog(
        initial_preset=LinePreset.Custom,
        initial_angle=45,
        merge_vertices=True,
        is_edit=True
    )
    line_dia.exec()

    print(f"{line_dia.preset=}\n"
          f"{line_dia.angle=}\n"
          f"{line_dia.merge_vertices=}\n"
          f"{line_dia.delete_flag=}")


def settings_dialog_test():
    settings_dialog = SettingsDialog()
    settings_dialog.exec()


def split_colour_dialog_test():
    colours= OrderedDict([
        ("Key_01_Main_Colour",[Brickcolour(16),[0,1]]),
        ("Key_02_Blue",[Brickcolour(1),[2,3]]),
        ("Key_03_Green",[Brickcolour(2),[4,5]]),
        ("Key_04_Red",[Brickcolour(4),[6,7]]),
    ])
    split_colour_dia = SplitColourDialog(colours)
    if split_colour_dia.exec():
        print(split_colour_dia.colour_groups)


def step_settings_dialog_test():
    line_dia = StepSettingsDialog()
    line_dia.exec()

    print(f"{line_dia.tol_linear=}\n"
          f"{line_dia.tol_angular=}\n"
          f"{line_dia.tol_relative=}\n")


if __name__ == "__main__":
    config, _ = loadconfig()
    basedir = os.path.dirname(__file__)
    basedir = basedir.removesuffix("tests")
    print(basedir)
    app = QApplication([0])
    if config["Theme"]["use_accent_colour"]:
        qdarktheme.setup_theme(config["Theme"]["mode"], custom_colors={"primary": config["Theme"]["accent_colour"]})
    else:
        qdarktheme.setup_theme(config["Theme"]["mode"])
    app.setWindowIcon(QIcon(os.path.join(basedir, "ThreeDToLD","icons", "3DToLD_icon.ico")))

    about_page_test(config)
    brick_colour_dialog_test()
    color_category_dialog_test()
    exception_dialog_test()
    line_generation_dialog_test()
    settings_dialog_test()
    split_colour_dialog_test()
    step_settings_dialog_test()