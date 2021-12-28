# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'iconedit.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IconEditWindow(object):
    def setupUi(self, IconEditWindow,lang):
        IconEditWindow.setObjectName("IconEditWindow")
        IconEditWindow.resize(394, 227)
        self.lang = lang
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
        IconEditWindow.setWindowTitle(self.lang.tr("edit_launch"))
        self.label.setText(self.lang.tr("title"))
        self.label_2.setText(self.lang.tr("icon_filename"))
        self.label_3.setText(self.lang.tr("launch_command"))
        self.okbtn.setText("OK")
        self.cancelbtn.setText(self.lang.tr("cancel"))
        
class IconEditWindow(QtWidgets.QDialog):
    def __init__(self, lang, parent= None):
        super(IconEditWindow, self).__init__(parent)
        self.ui = Ui_IconEditWindow()
        self.ui.setupUi(self,lang)
        self.ui.cancelbtn.clicked.connect(self.cancelclick)
        self.ui.okbtn.clicked.connect((self.okclick))
        self.setWindowFlags(QtCore.Qt.Tool)
       
    def cancelclick(self):
        self.reject()
    def okclick(self):
        self.accept()

def iconEdit(item, lang):
    ie = IconEditWindow(lang)
    ie.ui.eTitle.setText(item.title)
    ie.ui.eExec.setText(item.exec)
    ie.ui.eIcon.setText(item.icon)
    if ie.exec_() == 1:
        title = ie.ui.eTitle.text()
        icon = ie.ui.eIcon.text()
        exec = ie.ui.eExec.text()
        if len(icon) > 0 and len(exec) >0:
            shlIconChange = item.icon != icon
            item.title = title
            item.icon = icon
            item.exec = exec
            item.changeIcon()
            return True
    return False

def iconAdd(lang):
    ie = IconEditWindow(lang)
    if ie.exec_() == 1:
        title = ie.ui.eTitle.text()
        icon = ie.ui.eIcon.text()
        exec = ie.ui.eExec.text()
        if len(icon) > 0 and len(exec) >0:
            return True,title,icon,exec
    return False,'','',''
        
