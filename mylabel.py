# MyLabel class created only for emit mousemove and mousepress
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

class MyLabel(QtWidgets.QLabel):
    onMousePress = pyqtSignal(QMouseEvent)
    onMouseMove = pyqtSignal(QMouseEvent)

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.setMouseTracking(True)
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.onMousePress.emit(event)
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.onMouseMove.emit(event)

