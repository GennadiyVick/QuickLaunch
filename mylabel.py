# MyLabel class to emit mousemove
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
# 
#
# MyLabel class to emit mouse events
# Copyright (C) 2021  Roganov G.V. roganovg@mail.ru
#
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

class MyLabel(QtWidgets.QLabel):
    onMousePress = pyqtSignal(QMouseEvent)
    onMouseMove = pyqtSignal(QMouseEvent)
    onMouseRelease = pyqtSignal(QMouseEvent)

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.setMouseTracking(True)
        self.mx = 0
        self.my = 0
        
    def mousePressEvent(self, event):
        self.mx = event.globalX()
        self.my = event.globalY()
        if event.buttons() == Qt.LeftButton:
            self.onMousePress.emit(event)
    def mouseReleaseEvent(self, event):
        self.onMouseRelease.emit(event)
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.onMouseMove.emit(event)

