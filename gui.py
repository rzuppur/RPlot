#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2016 Reino Zuppur
reino.zuppur@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from PySide import QtGui, QtCore
from math import atan2, pi
import copy


# TODO: function typing delay
# TODO: reset button
# nice to have: real axis
# nice to have: resizable window

class Window(QtGui.QWidget):

    def __init__(self, rplot, width=400, height=300):
        super(Window, self).__init__()

        self.rplot = rplot
        self.image = None
        self.values = None
        self.coords = None

        self._wwidth = width
        self._wheight = height
        self._offset_x = 0
        self._offset_y = 0
        self._plot_scale = rplot.scale
        self._dragging = False
        self._lastcoords = [0,0]
        self._startcoords = [0, 0]
        self._worker_thread = None

        self._create_gui()
        self._create_image()

    def _create_gui(self):
        self._update_title()

        # CREATE LAYOUT
        self.resize(self._wwidth, self._wheight)
        self.setFixedSize(self.size())

        self.vbox = QtGui.QVBoxLayout(self)
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0,0,0,0)

        self.hbox = QtGui.QHBoxLayout()
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        # CREATE TEXTBOX
        self.tbox = QtGui.QLineEdit()
        self.tbox.setText(str(self.rplot))
        self.tbox.textChanged.connect(self._text_changed)
        self.tbox.setSelection(0,1000)
        self.hbox.addWidget(self.tbox)

        # CREATE LOG BUTTON
        self.lbut = QtGui.QCheckBox("USE LOG")
        self.lbut.setChecked(1)
        self.lbut.clicked.connect(self._toggle_log)
        self.lbut.setStyleSheet("background-color: #ffffff")
        self.hbox.addWidget(self.lbut)

        # CREATE NORM BUTTON
        self.nbut = QtGui.QCheckBox("USE NORMALIZATION")
        self.nbut.setChecked(1)
        self.nbut.clicked.connect(self._toggle_norm)
        self.nbut.setStyleSheet("background-color: #ffffff")
        self.hbox.addWidget(self.nbut)

        # CREATE IMAGE CONTAINER
        self.img = QtGui.QLabel(self)
        self.img.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.img.setMaximumSize(self._wwidth, self._wheight)
        self.setMouseTracking(1)
        self.img.setMouseTracking(1)
        self.vbox.addWidget(self.img)

        # CENTER WINDOW
        center = QtGui.QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(center)

        # SHOW GUI
        self.tbox.raise_()
        self.lbut.raise_()
        self.nbut.raise_()
        self.show()

    def _toggle_log(self):
        self.rplot.use_log = not self.rplot.use_log
        self._create_image()

    def _toggle_norm(self):
        self.rplot.use_normalization = not self.rplot.use_normalization
        self._create_image()

    def _text_changed(self, text):
        self.set_function(text)

    def _create_image(self):

        # SET VARIABLES
        self.rplot.h_size = self._wwidth
        self.rplot.v_size = self._wheight
        self.rplot.scale = self._plot_scale

        # CREATE WORKER THREAD
        self._stop_thread()
        self._worker_thread = RPlotThread(copy.copy(self.rplot))
        self._worker_thread.graafik.connect(self._set_image)
        self._worker_thread.values.connect(self._set_values)

        # START PLOTTING
        self._worker_thread.start()

    def _stop_thread(self):
        if self._worker_thread and self._worker_thread.isRunning():
            self._worker_thread.abort = True
            self._worker_thread.wait()

    def _set_image(self, img):
        self.image = img
        self.img.setPixmap(self.image.toqpixmap())
        #self.img.setMaximumSize(self._wwidth, self._wheight)
        #self.resize(self._wwidth, self._wheight)

    def _set_values(self, r):
        v, c = r
        self.coords = c
        self.values = v

    def _update_title(self):
        self.setWindowTitle('RPlot - ' + str(self.rplot))

    def _scale(self, amount):
        amount = int(amount)/1000 + 1
        if amount > 0:
            self._plot_scale *= amount
            px = self.img.pixmap()
            px = px.transformed(QtGui.QTransform().scale(amount, amount))
            self.img.setPixmap(px)
        else:
            self._plot_scale *= 1 / abs(amount)
            px = self.img.pixmap()
            px = px.transformed(QtGui.QTransform().scale(1-(1/abs(amount)), 1-(1/abs(amount))))
            self.img.setPixmap(px)

        self._create_image()

    # PUBLIC FUNCTIONS

    def set_function(self, function):
        """ Update function that RPlot shows.

        @param function: str   The function to draw ( for example "sin(z)" )
        @return:         None  None
        """
        self.rplot.function = function
        self._create_image()
        self._update_title()
        if self.tbox.text() != function:
            self.tbox.setText(function)

    def set_use_log(self, use):
        """ Set the checkbox to use or not to use logarithmic scale.

        @param use: bool  Use logarithmic scale to plot the function.
        @return:    bool  Was logarithmic scale used previously.
        """
        pv = self.rplot.use_log

        if use:
            self.lbut.setChecked(1)
            self.rplot.use_log = True
        else:
            self.lbut.setChecked(0)
            self.rplot.use_log = False

        self._create_image()
        return pv

    def set_use_normalization(self, use):
        """ Set the checkbox to use or not to use normalization for values ( "height lines" ).

        @param use: bool  Use normalization to plot the function.
        @return:    bool  Was normalization used previously.
        """
        pv = self.rplot.use_normalization

        if use:
            self.nbut.setChecked(1)
            self.rplot.use_normalization = True
        else:
            self.nbut.setChecked(0)
            self.rplot.use_normalization = False

        self._create_image()
        return pv

    # MOUSE AND KEYBOARD BINDINGS

    def mousePressEvent(self, e):
        if not self._dragging:
            self._dragging = True
            self._startcoords = [e.x(), e.y()]
            self._lastcoords = self._startcoords

    def mouseReleaseEvent(self, e):
        if self._dragging:
            self._dragging = False
            self.rplot.move(self._startcoords[0] - e.x(), e.y() - self._startcoords[1])
            self._create_image()

    def mouseMoveEvent(self, e):
        if self._dragging:
            self.img.move(self.img.x() + e.x() - self._lastcoords[0], self.img.y() + e.y() - self._lastcoords[1])
            self._lastcoords = [e.x(), e.y()]
        else:
            try:
                z = self.values[e.y() - self.img.y(), e.x()]
                coords = self.coords[0][0][e.x()], self.coords[1][e.y() - self.img.y()][0]

                z_argument = str(round(180*atan2(z.imag, z.real)/pi, 1)) + "°"
                z_a = str(round(z.real, 2)) + " + "+str(round(z.imag, 2)) + "i"
                z_b = str(round(abs(z), 2))+"∠" + z_argument
                z_c = "x:" + str(round(coords[0], 2)) + " y:" + str(round(coords[1], 2))
                s = z_a +"\n" + z_b + "\n" + z_c
                QtGui.QToolTip.showText(e.globalPos(), s)
            except:
                pass

    def wheelEvent(self, e):
        self._scale(e.delta())

    def keyPressEvent(self, e):
        key = e.key()

        if key == QtCore.Qt.Key_PageUp:
            self._scale(200)
        elif key == QtCore.Qt.Key_PageDown:
            self._scale(-200)
        elif key == QtCore.Qt.Key_F1:
            self.lbut.nextCheckState()
            self._toggle_log()
        elif key == QtCore.Qt.Key_F2:
            self.nbut.nextCheckState()
            self._toggle_norm()


class RPlotThread(QtCore.QThread):

    # TODO: faster aborting of old threads

    graafik = QtCore.Signal(object)
    values = QtCore.Signal(object)

    def __init__(self, rplot):
        QtCore.QThread.__init__(self)
        self.rplot = rplot
        self.abort = False

    def run(self):
        self.rplot.create_graph()
        if not self.abort:
            self.graafik.emit(self.rplot.get_image())
            self.values.emit(self.rplot.get_values())


def create_app(arg):
    return QtGui.QApplication(arg)
