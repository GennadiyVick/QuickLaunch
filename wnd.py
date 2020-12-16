# -*- coding: utf-8 -*-
# Initializing mainwindow interface
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
#
# some else...
# I bag your pardon for russian documentation of functions,



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from mylabel import MyLabel



class Ui_PanelWindow(object):
    def __init__(self):
        self.width = 206
        self.height = 122
    def setupUi(self, PanelWindow):
        """Инициализируем графический интерфейс главного окна,
           создаём необходимые компоненты на форме и задаём их свойства."""        
        PanelWindow.setObjectName("PanelWindow")
        PanelWindow.setFixedSize(QSize(self.width, self.height))

        #фон окна прозрачный чтобы можно было в стиле установить любой цвет с альфой
        PanelWindow.setStyleSheet("background: transparent;") 
        PanelWindow.setAttribute(Qt.WA_TranslucentBackground)

        #FramelessWindowHint - окно без рамок,
        #Qt.Tool - чтобы небыло видно иконки на панели задач
        
        PanelWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool) # | Qt.WindowStaysOnTopHint  | Qt.Tool

        self.centralwidget = QtWidgets.QWidget(PanelWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {\n"
            "background: #50000000;\n"
            "border-style: inset;\n"
            "border-width: 1px;\n"
            "border-color: #90404050;\n"
            "border-radius: 10px;}")
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(4, 3, 3, 3)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ltitle = MyLabel(self.centralwidget) #QtWidgets.QLabel(self.centralwidget)
        self.ltitle.setAlignment(QtCore.Qt.AlignCenter)
        self.ltitle.setObjectName("ltitle")
        self.ltitle.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ltitle.setMaximumSize(QtCore.QSize(self.width, 30))
        self.verticalLayout.addWidget(self.ltitle)

        if isinstance(PanelWindow, QtWidgets.QMainWindow):
            PanelWindow.setCentralWidget(self.centralwidget)
        else:
            ml = QtWidgets.QVBoxLayout(PanelWindow)
            ml.setContentsMargins(0, 0, 0, 0)
            ml.setSpacing(0)
            ml.setObjectName("ml")
            ml.addWidget(self.centralwidget)

        self.retranslateUi(PanelWindow)
        QtCore.QMetaObject.connectSlotsByName(PanelWindow)
        

    def retranslateUi(self, PanelWindow):
        pass
        #_translate = QtCore.QCoreApplication.translate
        #PanelWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
