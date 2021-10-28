from PyQt5.QtWidgets import QDialog, QColorDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from settingsdialogwindow import Ui_Dialog


class SettingsDialog(QDialog):
    def __init__(self, sets,parent = None):
        super(SettingsDialog,self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.sets = sets
        self.lvmodel = QStandardItemModel(self);
        self.ui.lv.setModel(self.lvmodel)
        setpages = ['Панель иконок','Настройка окна','Настройка группы']
        for page in setpages:
            item = QStandardItem(page)
            self.lvmodel.appendRow(item)
        self.ui.lv.clicked.connect(self.lvclicked)
        self.ui.lv.setCurrentIndex(self.lvmodel.index(0,0))
        self.ui.bOk.clicked.connect(self.okClick)
        self.ui.bCancel.clicked.connect(self.cancelClick)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.initButtons()

    def getcol(self,label):
        st = label.styleSheet()
        return st.replace('background: ','').replace(';','')

    def setcol(self,lab,key):
        lab.setStyleSheet('background: '+self.sets.get(key,self.getcol(lab))+';')

    def setsbv(self,sb,key):
        sb.setValue(self.sets.get(key,sb.value()))

    def setcbv(self,cb,key):
        cb.setChecked(self.sets.get(key,cb.isChecked()))


    def loadfromsets(self):
        self.ui.pEdit.setPlainText(self.sets.get('window.style',self.ui.pEdit.toPlainText()))
        self.updatestyle()
        self.setcol(self.ui.lTitleColor,'window.titlecolor')
        self.setcol(self.ui.lMenuColor,'window.menucolor')
        self.setcol(self.ui.lMenuBgColor,'window.menubgcolor')

        self.setsbv(self.ui.sbDefaultIconSize,'panel.defaulticonsize')
        self.setsbv(self.ui.sbIconSize,'panel.iconsize')
        self.setsbv(self.ui.sbScaledIconSize,'panel.scalediconsize')
        self.setsbv(self.ui.dsbShaddowOffsetX,'panel.shaddowoffsetx')
        #self.setsbv(self.ui.dsbShaddowOffsetY,'panel.shaddowoffsety')
        self.setsbv(self.ui.dsbShaddowGause,'panel.shaddowgause')
        self.setcol(self.ui.lShaddowColor,'panel.shaddowcolor')
        self.setcol(self.ui.lTextColor,'panel.textcolor')
        self.setcbv(self.ui.cbWithText,'panel.withtext')
        self.setcbv(self.ui.cbShaddow,'panel.shaddow')

        self.setcol(self.ui.lGroupTitleColor,'group.titlecolor')
        self.setcol(self.ui.lGroupTitleBgColor,'group.titlebgcolor')
        self.setcol(self.ui.lGroupTitleBorderColor,'group.titlebordercolor')

        self.ui.eTitle.setText(self.sets.get('title',''))


    def savetosets(self):
        self.sets.set('window.style',self.ui.pEdit.toPlainText())
        self.sets.set('window.titlecolor',self.getcol(self.ui.lTitleColor))
        self.sets.set('window.menucolor',self.getcol(self.ui.lMenuColor))
        self.sets.set('window.menubgcolor',self.getcol(self.ui.lMenuBgColor))

        self.sets.set('panel.defaulticonsize',self.ui.sbDefaultIconSize.value())
        self.sets.set('panel.iconsize',self.ui.sbIconSize.value())
        self.sets.set('panel.scalediconsize',self.ui.sbScaledIconSize.value())
        self.sets.set('panel.shaddowoffsetx',self.ui.dsbShaddowOffsetX.value())
        #self.sets.set('panel.shaddowoffsety',self.ui.dsbShaddowOffsetY.value())
        self.sets.set('panel.shaddowgause',self.ui.dsbShaddowGause.value())
        self.sets.set('panel.shaddowcolor',self.getcol(self.ui.lShaddowColor))
        self.sets.set('panel.textcolor',self.getcol(self.ui.lTextColor,))
        self.sets.set('panel.withtext',self.ui.cbWithText.isChecked())
        self.sets.set('panel.shaddow',self.ui.cbShaddow.isChecked())

        self.sets.set('group.titlecolor',self.getcol(self.ui.lGroupTitleColor))
        self.sets.set('group.titlebgcolor',self.getcol(self.ui.lGroupTitleBgColor))
        self.sets.set('group.titlebordercolor',self.getcol(self.ui.lGroupTitleBorderColor))

        self.sets.set('title',self.ui.eTitle.text())

    def initButtons(self):
        self.ui.bUpdate.clicked.connect(self.updatestyle)
        self.ui.bTitleColor.clicked.connect(self.chtitlecolor)
        self.ui.bMenuColor.clicked.connect(self.chmenucolor)
        self.ui.bMenuBgColor.clicked.connect(self.chmenubgcolor)
        self.ui.bShaddowColor.clicked.connect(self.chshaddowcolor)
        self.ui.bTextColor.clicked.connect(self.chtextcolor)
        self.ui.bGroupTitleColor.clicked.connect(self.chgrouptitlecolor)
        self.ui.bGroupTitleBgColor.clicked.connect(self.chgrouptitlebgcolor)
        self.ui.bGroupTitleBorderColor.clicked.connect(self.chgrouptitlebordercolor)

    def getDlgClr(self,default):
        dlg = QColorDialog(QColor(default),self)
        dlg.setOption(QColorDialog.ShowAlphaChannel, on=True)
        if dlg.exec() == 1:
            return dlg.selectedColor().name(QColor.HexArgb)
        else: return default

    def chcol(self,label):
        col = self.getDlgClr(self.getcol(label))
        label.setStyleSheet("background: "+col+";")

    def lvclicked(self,index):
        i = index.row()
        self.ui.stackedWidget.setCurrentIndex(i)
        #venue = self.model().data(index, VenueListModel.VenueRole)

    def updatestyle(self):
        self.ui.centralwidget.setStyleSheet(self.ui.pEdit.toPlainText())

    def chtitlecolor(self):
        self.chcol(self.ui.lTitleColor)

    def chmenucolor(self):
        self.chcol(self.ui.lMenuColor)

    def chmenubgcolor(self):
        self.chcol(self.ui.lMenuBgColor)

    def chshaddowcolor(self):
        self.chcol(self.ui.lShaddowColor)

    def chtextcolor(self):
        self.chcol(self.ui.lTextColor)

    def chgrouptitlecolor(self):
        self.chcol(self.ui.lGroupTitleColor)

    def chgrouptitlebgcolor(self):
        self.chcol(self.ui.lGroupTitleBgColor)

    def chgrouptitlebordercolor(self):
        self.chcol(self.ui.lGroupTitleBorderColor)


    def okClick(self):
        self.accept()

    def cancelClick(self):
        self.reject()
