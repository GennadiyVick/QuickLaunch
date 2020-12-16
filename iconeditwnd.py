# IconEditWindow dialog
# Create graphic interface for a window of iconinfo editing 
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


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IconEditWindow(object):
    def setupUi(self, IconEditWindow):
        IconEditWindow.setObjectName("IconEditWindow")
        IconEditWindow.resize(394, 227)
        self.verticalLayout = QtWidgets.QVBoxLayout(IconEditWindow)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(IconEditWindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.eTitle = QtWidgets.QLineEdit(IconEditWindow)
        self.eTitle.setObjectName("eTitle")
        self.verticalLayout.addWidget(self.eTitle)
        self.label_2 = QtWidgets.QLabel(IconEditWindow)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.eIcon = QtWidgets.QLineEdit(IconEditWindow)
        self.eIcon.setObjectName("eIcon")
        self.verticalLayout.addWidget(self.eIcon)
        self.label_3 = QtWidgets.QLabel(IconEditWindow)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.eExec = QtWidgets.QLineEdit(IconEditWindow)
        self.eExec.setObjectName("eExec")
        self.verticalLayout.addWidget(self.eExec)
        self.widget = QtWidgets.QWidget(IconEditWindow)
        self.widget.setMinimumSize(QtCore.QSize(0, 45))
        self.widget.setObjectName("widget")
        self.okbtn = QtWidgets.QPushButton(self.widget)
        self.okbtn.setGeometry(QtCore.QRect(175, 9, 88, 34))
        self.okbtn.setObjectName("okbtn")
        self.cancelbtn = QtWidgets.QPushButton(self.widget)
        self.cancelbtn.setGeometry(QtCore.QRect(285, 9, 88, 34))
        self.cancelbtn.setObjectName("cancelbtn")
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(IconEditWindow)
        QtCore.QMetaObject.connectSlotsByName(IconEditWindow)

    def retranslateUi(self, IconEditWindow):
        _translate = QtCore.QCoreApplication.translate
        IconEditWindow.setWindowTitle(_translate("IconEditWindow", "Редактировать запуск"))
        self.label.setText(_translate("IconEditWindow", "Заголовок"))
        self.label_2.setText(_translate("IconEditWindow", "Файл иконки"))
        self.label_3.setText(_translate("IconEditWindow", "Комманда запуска"))
        self.okbtn.setText(_translate("IconEditWindow", "OK"))
        self.cancelbtn.setText(_translate("IconEditWindow", "Отмена"))
        
class IconEditWindow(QtWidgets.QDialog):
    def __init__(self, parent= None):
        super(IconEditWindow, self).__init__(parent)
        self.ui = Ui_IconEditWindow()
        self.ui.setupUi(self)
        self.ui.cancelbtn.clicked.connect(self.cancelclick)
        self.ui.okbtn.clicked.connect((self.okclick))
        self.setWindowFlags(QtCore.Qt.Tool)
       
    def cancelclick(self):
        self.reject()
    def okclick(self):
        self.accept()      
        
