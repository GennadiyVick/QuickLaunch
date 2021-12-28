# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupedit.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog, lang):
        Dialog.setObjectName("Dialog")
        Dialog.resize(302, 125)
        self.lang = lang
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addWidget(self.widget)
        self.cbiconwithtext = QtWidgets.QCheckBox(Dialog)
        self.cbiconwithtext.setObjectName("cbiconwithtext")
        self.verticalLayout.addWidget(self.cbiconwithtext)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(self.lang.tr("icon_group"))
        self.label.setText(self.lang.tr("title"))
        self.cbiconwithtext.setText(self.lang.tr("icon_viewlist"))

class GroupEditWindow(QtWidgets.QDialog):
    def __init__(self, lang, parent= None):
        super(GroupEditWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self,lang)
        #self.ui.cancelbtn.clicked.connect(self.cancelclick)
        #self.ui.okbtn.clicked.connect((self.okclick))
        self.setWindowFlags(QtCore.Qt.Tool)

def groupEdit(group, lang):
    ge = GroupEditWindow(lang)
    title = group.title
    withtext = group.withtext
    ge.ui.lineEdit.setText(title)
    ge.ui.cbiconwithtext.setChecked(withtext)
    if ge.exec_() == 1:
        title = ge.ui.lineEdit.text()
        withtext = ge.ui.cbiconwithtext.isChecked()
    return title, withtext

def groupAdd(lang,withText = False):
    ge = GroupEditWindow(lang)
    title = ''
    withtext = withText
    ge.ui.lineEdit.setText(title)
    ge.ui.cbiconwithtext.setChecked(withtext)
    if ge.exec_() == 1:
        title = ge.ui.lineEdit.text()
        withtext = ge.ui.cbiconwithtext.isChecked()
        return True, title, withtext
    return False, title, withtext

