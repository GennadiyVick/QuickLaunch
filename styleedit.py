# -*- coding: utf-8 -*-
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QColor

class Ui_Dialog(object):
    def setupUi(self, Dialog, textcolor = QColor(255,255,255)):
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
        
        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setMinimumSize(QtCore.QSize(0, 35))
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.clr = QtWidgets.QLabel(self.widget_5)
        self.clr.setMinimumSize(QtCore.QSize(30, 30))
        self.clr.setMaximumSize(QtCore.QSize(33, 16777215))
        self.clr.setStyleSheet("background: "+textcolor.name()+";")
        self.clr.setText("")
        self.clr.setObjectName("clr")
        self.horizontalLayout_3.addWidget(self.clr)
        self.bClr = QtWidgets.QPushButton(self.widget_5)
        self.bClr.setObjectName("bClr")
        self.horizontalLayout_3.addWidget(self.bClr)
        self.verticalLayout_2.addWidget(self.widget_5)        
        
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
        Dialog.setWindowTitle(_translate("Dialog", "Стиль фона панели, цвет текста"))
        self.label.setText(_translate("Dialog", "Текст стиля"))
        self.label_2.setText(_translate("Dialog", "Пример"))
        self.bUpdate.setText(_translate("Dialog", "Обновить пример"))
        self.bOk.setText(_translate("Dialog", "OK"))
        self.bCancel.setText(_translate("Dialog", "Отмена"))
        self.bClr.setText(_translate("Dialog", "Цвет текста заголовка"))        

class StyleEditWindow(QtWidgets.QDialog):
    def __init__(self, parent= None, textColor = QColor(255,255,255)):
        super(StyleEditWindow, self).__init__(parent)
        self.tcolor = textColor
        self.ui = Ui_Dialog()
        self.ui.setupUi(self,self.tcolor)
        self.ui.bCancel.clicked.connect(self.cancelclick)
        self.ui.bOk.clicked.connect((self.okclick))
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setStyleSheet("background: #222; color: #aaa;")
        self.ui.bUpdate.clicked.connect(self.updateclick)
        self.ui.bClr.clicked.connect(self.textcolorclick)
        
       
    def cancelclick(self):
        self.reject()
    def okclick(self):
        self.accept() 
    def updateclick(self):
        self.ui.centralwidget.setStyleSheet(self.ui.pEdit.toPlainText())    
    def textcolorclick(self):
        self.tcolor = QColorDialog.getColor()
        self.ui.clr.setStyleSheet("background: "+self.tcolor.name()+";")
        

