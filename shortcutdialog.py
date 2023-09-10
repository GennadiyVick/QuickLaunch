from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ShortcutDialog(object):
    def setupUi(self, ShortcutDialog, lang):
        self.lang = lang
        ShortcutDialog.setObjectName("ShortcutDialog")
        ShortcutDialog.resize(338, 126)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShortcutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lshortcut = QtWidgets.QLabel(ShortcutDialog)
        self.lshortcut.setWordWrap(True)
        self.lshortcut.setObjectName("lshortcut")
        self.verticalLayout.addWidget(self.lshortcut)
        self.hl = QtWidgets.QHBoxLayout()
        self.hl.setObjectName("hl")
        self.ke = QtWidgets.QKeySequenceEdit(ShortcutDialog)
        self.ke.setObjectName("ke")
        self.hl.addWidget(self.ke)
        self.bClear = QtWidgets.QPushButton(ShortcutDialog)
        self.bClear.setObjectName("bClear")
        self.hl.addWidget(self.bClear)
        self.verticalLayout.addLayout(self.hl)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.box = QtWidgets.QDialogButtonBox(ShortcutDialog)
        self.box.setOrientation(QtCore.Qt.Horizontal)
        self.box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.box.setObjectName("box")
        self.verticalLayout.addWidget(self.box)

        self.retranslateUi(ShortcutDialog)
        self.box.accepted.connect(ShortcutDialog.accept) # type: ignore
        self.box.rejected.connect(ShortcutDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ShortcutDialog)

    def retranslateUi(self, ShortcutDialog):
        ShortcutDialog.setWindowTitle(self.lang.tr("shortcut"))
        self.lshortcut.setText(self.lang.tr("visible_shortcut"))
        self.bClear.setText(self.lang.tr("clear"))

class ShortcutDialog(QtWidgets.QDialog):
    def __init__(self, lang, parent=None):
        super(ShortcutDialog,self).__init__(parent)
        self.lang = lang
        self.ui = Ui_ShortcutDialog()
        self.ui.setupUi(self,lang)
        self.ui.bClear.clicked.connect(self.ui.ke.clear)

    def accept(self):
        if self.ui.ke.keySequence().count() == 0:
            return
        else:
            super().accept()


def getShortCut(lang, parent):
    dlg = ShortcutDialog(lang, parent)
    if dlg.exec() == 1:
        if dlg.ui.ke.keySequence().count() > 0:
            return dlg.ui.ke.keySequence()[0]
        else: return None
    else:
        return None
