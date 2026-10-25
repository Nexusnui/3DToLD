# ------------------------------------- #
#                                       #
# Modern Color Picker by Tom F.         #
# Edited by GiorgosXou for Qt6 Support. #
# Edited by Nexusnui to fix issue with  #
# QPoint and add QColor to colorChanged #
#                                       #
# Version 1.3.1                         #
# made with Qt Creator & PyQt5          #
#                                       #
# ------------------------------------- #

import colorsys

from PyQt6.QtCore import (Qt, pyqtSignal, QPointF)
from PyQt6.QtWidgets import QWidget

from .ui_main import Ui_ColorPicker as Ui_Main


class ColorPicker(QWidget):
    colorChanged = pyqtSignal(str)

    def __init__(self, *args, **kwargs):

        # Extract Initial Color out of kwargs
        rgb = kwargs.pop("rgb", None)
        rgba = kwargs.pop("rgba", None)
        hsv = kwargs.pop("hsv", None)
        hex = kwargs.pop("hex", None)

        super(ColorPicker, self).__init__(*args, **kwargs)

        # Call UI Builder function
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        # Connect update functions
        self.ui.hue.mouseMoveEvent = self.moveHueSelector
        self.ui.hue.mousePressEvent = self.moveHueSelector
        self.ui.red.textEdited.connect(self.rgbaChanged)
        self.ui.green.textEdited.connect(self.rgbaChanged)
        self.ui.blue.textEdited.connect(self.rgbaChanged)
        self.ui.alpha.textEdited.connect(self.rgbaChanged)
        self.ui.hex.textEdited.connect(self.hexChanged)

        # Connect selector moving function
        self.ui.black_overlay.mouseMoveEvent = self.moveSVSelector
        self.ui.black_overlay.mousePressEvent = self.moveSVSelector

        if rgb:
            self.setRGBA((*rgb, 255))
        elif rgba:
            self.setRGBA(rgba)
        elif hsv:
            self.setHSV((*hsv, 255))
        elif hex:
            self.setHex(hex)
        else:
            self.setRGBA((0, 0, 0, 255))

    ## Main Functions ##
    def getHSV(self, hrange=100, svrange=100):
        h, s, v, a = self.color
        return h * (hrange / 100.0), s * (svrange / 100.0), v * (svrange / 100.0), a

    def getRGBA(self, range=255):
        r, g, b, a = self.i(self.ui.red.text()), self.i(self.ui.green.text()), self.i(self.ui.blue.text()), self.i(self.ui.alpha.text())
        return int(r * (range / 255.0)), int(g * (range / 255.0)), int(b * (range / 255.0)), int(a * (range / 255.0))

    def getHex(self, ht=False):
        rgba = (self.i(self.ui.red.text()), self.i(self.ui.green.text()), self.i(self.ui.blue.text()), self.i(self.ui.alpha.text()))
        if ht:
            return "#" + self.rgba2hex(rgba)
        else:
            return self.rgba2hex(rgba)

    ## Update Functions ##
    def hsvChanged(self):
        h, s, v = (
            100 - self.ui.hue_selector.y() / 1.85, (self.ui.selector.x() + 6) / 2.0, (194 - self.ui.selector.y()) / 2.0)
        a = self.i(self.ui.alpha.text())
        r, g, b, a = self.hsv2rgba(h, s, v, a)
        self.color = (h, s, v, a)
        self._setRGBA((r, g, b, a))
        self._setHex(self.hsv2hex(self.color))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")
        self.ui.color_view.setStyleSheet(
            f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({h}%,100%,50%), stop:1 #fff);")
        self.colorChanged.emit(self.getHex(True))

    def rgbaChanged(self):
        r, g, b, a = self.i(self.ui.red.text()), self.i(self.ui.green.text()), self.i(self.ui.blue.text()), self.i(self.ui.alpha.text())
        self.color = self.rgba2hsv(r, g, b, a)
        self._setHSV(self.color)
        self._setHex(self.rgba2hex((r, g, b, a)))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")
        self.colorChanged.emit(self.getHex(True))

    def hexChanged(self):
        hex = self.ui.hex.text()
        r, g, b, a = self.hex2rgba(hex)
        self.color = self.hex2hsv(hex)
        self._setHSV(self.color)
        self._setRGBA((r, g, b, a))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")
        self.colorChanged.emit(self.getHex(True))

    ## internal setting functions ##
    def _setRGBA(self, c):
        r, g, b, a = c
        self.ui.red.setText(str(self.i(r)))
        self.ui.green.setText(str(self.i(g)))
        self.ui.blue.setText(str(self.i(b)))
        self.ui.alpha.setText(str(self.i(a)))

    def _setHSV(self, c):
        self.ui.hue_selector.move(QPointF(7, (100 - c[0]) * 1.85).toPoint())
        self.ui.color_view.setStyleSheet(
            f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({c[0]}%,100%,50%), stop:1 #fff);")
        self.ui.selector.move(QPointF(c[1] * 2 - 6, (200 - c[2] * 2) - 6).toPoint())

    def _setHex(self, c):
        self.ui.hex.setText(c)

    ## external setting functions ##
    def setRGBA(self, c):
        self._setRGBA(c)
        self.rgbaChanged()

    def setHSV(self, c):
        self._setHSV(c)
        self.hsvChanged()

    def setHex(self, c):
        self._setHex(c)
        self.hexChanged()

    ## Color Utility ##
    def hsv2rgba(self, h_or_color, s=0, v=0, a=0):
        if type(h_or_color).__name__ == "tuple":
            h, s, v, a = h_or_color
        else:
            h = h_or_color
        r, g, b = colorsys.hsv_to_rgb(h / 100.0, s / 100.0, v / 100.0)
        return *self.clampRGB((r * 255, g * 255, b * 255)), a

    def rgba2hsv(self, r_or_color, g=0, b=0, a=0):
        if type(r_or_color).__name__ == "tuple":
            r, g, b, a = r_or_color
        else:
            r = r_or_color
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        return h * 100, s * 100, v * 100, a

    def hex2rgba(self, hex_value):
        if len(hex_value) < 8:
            hex_value += "0" * (8 - len(hex_value))
        elif len(hex_value) > 8:
            hex_value = hex_value[0:8]
        rgba = tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4, 6))
        return rgba

    def rgba2hex(self, r_or_color, g=0, b=0, a=0):
        if type(r_or_color).__name__ == "tuple":
            r, g, b, a = r_or_color
        else:
            r = r_or_color
        hex_value = '%02x%02x%02x%02x' % (int(r), int(g), int(b), int(a))
        return hex_value

    def hex2hsv(self, hex_value):
        return self.rgba2hsv(self.hex2rgba(hex_value))

    def hsv2hex(self, h_or_color, s=0, v=0, a=0):
        if type(h_or_color).__name__ == "tuple":
            h, s, v, a = h_or_color
        else:
            h = h_or_color
        return self.rgba2hex(self.hsv2rgba(h, s, v, a))

    # selector move function
    def moveSVSelector(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if pos.x() < 0:
                pos.setX(0)
            if pos.y() < 0:
                pos.setY(0)
            if pos.x() > 230:
                pos.setX(230)
            if pos.y() > 230:
                pos.setY(230)
            self.ui.selector.move(QPointF(pos.x() - 6, pos.y() - 6).toPoint())
            self.hsvChanged()

    def moveHueSelector(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position().y() - 7
            if pos < 0:
                pos = 0
            if pos > 185:
                pos = 185
            self.ui.hue_selector.move(QPointF(7, pos).toPoint())
            self.hsvChanged()

    def i(self, text):
        try:
            return int(text)
        except:
            return 0

    def clampRGB(self, rgb):
        r, g, b = rgb
        if r < 0.0001:
            r = 0
        if g < 0.0001:
            g = 0
        if b < 0.0001:
            b = 0
        if r > 255:
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255
        return r, g, b
