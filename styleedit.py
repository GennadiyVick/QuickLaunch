# StyleEditWindow dialog
# Create graphic interface for a window of panel style editing 
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(414, 243)
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_3)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pEdit = QtWidgets.QPlainTextEdit(self.widget_3)
        self.pEdit.setObjectName("pEdit")
        self.verticalLayout_2.addWidget(self.pEdit)
        self.horizontalLayout.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.centralwidget = QtWidgets.QGraphicsView(self.widget_4)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3.addWidget(self.centralwidget)
        self.bUpdate = QtWidgets.QPushButton(self.widget_4)
        self.bUpdate.setObjectName("bUpdate")
        self.verticalLayout_3.addWidget(self.bUpdate)
        self.horizontalLayout.addWidget(self.widget_4)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(-1, 6, -1, 6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(193, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.bOk = QtWidgets.QPushButton(self.widget)
        self.bOk.setObjectName("bOk")
        self.horizontalLayout_2.addWidget(self.bOk)
        self.bCancel = QtWidgets.QPushButton(self.widget)
        self.bCancel.setObjectName("bCancel")
        self.horizontalLayout_2.addWidget(self.bCancel)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Текст стиля"))
        self.label_2.setText(_translate("Dialog", "Пример"))
        self.bUpdate.setText(_translate("Dialog", "Обновить пример"))
        self.bOk.setText(_translate("Dialog", "OK"))
        self.bCancel.setText(_translate("Dialog", "Отмена"))

class StyleEditWindow(QtWidgets.QDialog):
    def __init__(self, parent= None):
        super(StyleEditWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.bCancel.clicked.connect(self.cancelclick)
        self.ui.bOk.clicked.connect((self.okclick))
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setStyleSheet("background: #222;")
        self.ui.bUpdate.clicked.connect(self.updateclick)
        
       
    def cancelclick(self):
        self.reject()
    def okclick(self):
        self.accept() 
    def updateclick(self):
        self.ui.centralwidget.setStyleSheet(self.ui.pEdit.toPlainText())     

