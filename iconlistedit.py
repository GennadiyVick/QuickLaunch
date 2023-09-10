#
# Icon list
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
#
from PyQt5 import QtCore, QtGui, QtWidgets
import images
import sys
import iconedit
from myitem import iconFromName
from groupedit import groupedit

class MyLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.clicked.emit()

class Ui_IconListDialog(object):
    def setupUi(self, IconListDialog, lang):
        IconListDialog.setObjectName("IconListDialog")
        IconListDialog.resize(411, 396)
        IconListDialog.setStyleSheet("Background: #333;")
        self.lang = lang
        self.verticalLayout = QtWidgets.QVBoxLayout(IconListDialog)
        self.verticalLayout.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(IconListDialog)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lv = QtWidgets.QListView(self.widget)
        self.lv.setStyleSheet("QListView {\n"
"    background: rgba(0, 0, 0, 60);\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #445;\n"
"    color: #bbb;\n"
"    border-radius: 10px;\n"
"}\n"
"QListView::item:selected { background: rgba(0, 0, 0, 60); border-width: 1px; border-style: inset; border-color: #345; border-radius: 6px; color: #fff;}\n"
"QListView::item:focus { background: rgba(0, 30, 60, 90); border-width: 1px; border-style: inset; border-color: #345; border-radius: 6px; color: #ddd;}\n"
"QListView::item:focus:hover { background: rgba(0, 30, 60, 90); color: #fff;}\n"
"QListView::item:hover { background: transparent; color: #eee;}\n"
"QListView::item:selected:hover {background: rgba(0, 0, 0, 60); color:  aqua;}\n"
"")
        self.lv.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lv.setIconSize(QtCore.QSize(32, 32))
        self.lv.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lv.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.lv.setObjectName("lv")
        self.horizontalLayout.addWidget(self.lv)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setMinimumSize(QtCore.QSize(52, 0))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lAdd = MyLabel(self.widget_2)
        self.lAdd.setMinimumSize(QtCore.QSize(48, 48))
        self.lAdd.setStyleSheet("QLabel  {background:  url(\":/iadd.png\")}\n"
"QLabel:hover {background:  url(\":/iadd_h.png\")}\n"
"")
        self.lAdd.setLineWidth(0)
        self.lAdd.setText("")
        self.lAdd.setObjectName("lAdd")
        self.verticalLayout_2.addWidget(self.lAdd)
        self.lEdit = MyLabel(self.widget_2)
        self.lEdit.setMinimumSize(QtCore.QSize(48, 48))
        self.lEdit.setStyleSheet("QLabel  {background:  url(\":/iedit.png\")}\n"
"QLabel:hover {background:  url(\":/iedit_h.png\")}\n"
"")
        self.lEdit.setLineWidth(0)
        self.lEdit.setText("")
        self.lEdit.setObjectName("lEdit")
        self.verticalLayout_2.addWidget(self.lEdit)
        self.lDel = MyLabel(self.widget_2)
        self.lDel.setMinimumSize(QtCore.QSize(48, 48))
        self.lDel.setStyleSheet("QLabel  {background:  url(\":/idel.png\")}\n"
"QLabel:hover {background:  url(\":/idel_h.png\")}\n"
"")
        self.lDel.setLineWidth(0)
        self.lDel.setText("")
        self.lDel.setObjectName("lDel")
        self.verticalLayout_2.addWidget(self.lDel)
        self.lUp = MyLabel(self.widget_2)
        self.lUp.setMinimumSize(QtCore.QSize(48, 48))
        self.lUp.setStyleSheet("QLabel  {background:  url(\":/up.png\")}\n"
"QLabel:hover {background:  url(\":/up_h.png\")}\n"
"")
        self.lUp.setText("")
        self.lUp.setObjectName("lUp")
        self.verticalLayout_2.addWidget(self.lUp)
        self.lDown = MyLabel(self.widget_2)
        self.lDown.setMinimumSize(QtCore.QSize(48, 48))
        self.lDown.setStyleSheet("QLabel  {background:  url(\":/down.png\")}\\nQLabel:hover {background:  url(\":/down_h.png\")}\\n")
        self.lDown.setText("")
        self.lDown.setObjectName("lDown")
        self.verticalLayout_2.addWidget(self.lDown)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(IconListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(IconListDialog)
        self.buttonBox.accepted.connect(IconListDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(IconListDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(IconListDialog)

    def retranslateUi(self, IconListDialog):
        IconListDialog.setWindowTitle(self.lang.tr('iconlisttitle'))
        self.lAdd.setToolTip(self.lang.tr('add_link'))
        self.lEdit.setToolTip(self.lang.tr('edit_launch'))
        self.lDel.setToolTip(self.lang.tr('remove'))


class Item(QtGui.QStandardItem):
    def __init__(self, icon = None, title = '', iconfn = '', exec = '', groupindex = 0, isgroup = False, itemindex = 0):
        if icon != None:
            super(Item,self).__init__(icon, title)
        else:
            super(Item,self).__init__(title)
        self.groupindex = groupindex
        self.isgroup = isgroup
        self.itemindex = itemindex
        self.iconfn = iconfn
        self.title = title
        self.exec = exec
        self.withtext = False

    def assign(self, item):
        self.setIcon(item.icon())
        self.setText(item.text())
        self.groupindex = item.groupindex
        self.isgroup = item.isgroup
        self.itemindex = item.itemindex
        self.iconfn = item.iconfn
        self.title = item.title
        self.exec = item.exec



class IconListDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, lang = None):
        super(IconListDialog, self).__init__(None)
        self.panel = parent
        self.ui = Ui_IconListDialog()
        self.ui.setupUi(self, lang) #,self.lang)
        self.lang = lang
        #self.glist = self.panel.glist.copy()
        self.model = QtGui.QStandardItemModel(self)
        self.ui.lv.setModel(self.model)
        self.ui.lv.doubleClicked.connect(self.editselected)
        self.ui.lEdit.clicked.connect(self.editselected)
        self.ui.lAdd.clicked.connect(self.additem)
        self.ui.lDel.clicked.connect(self.delitem)
        self.ui.lUp.clicked.connect(self.moveup)
        self.ui.lDown.clicked.connect(self.movedown)
        for i in range(len(self.panel.glist)):
            il = self.panel.glist[i]
            gitem = Item(None,il.titletext, '', '', i, True)
            gitem.withtext = il.withtext
            self.model.appendRow(gitem)
            for j in range(len(il)):
                ii = il[j]
                item = Item(QtGui.QIcon(ii.pixmap()), ii.title, ii.icon, ii.exec, i, itemindex=j)
                self.model.appendRow(item)
            #self.model.appendRow(QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(fn)))

    def additem(self):
        r, title, icon, exec = iconedit.iconAdd(self.lang)
        if not r: return
        if self.model.rowCount == 0:
            gitem = Item(title='', isgroup=True)
            gitem.withtext = False
            self.model.appendRow(gitem)
        i =  self.ui.lv.currentIndex().row()

        if i < 0:
            i = 1
        else:
            gi = 0
            for n in range(i, -1, -1):
                if self.model.item(n).isgroup:
                    gi = n
                    break
            i = self.model.rowCount()
            for n in range(gi+1,self.model.rowCount()):
                if self.model.item(n).isgroup:
                    i = n-1
                    break
        item = Item(iconFromName(icon), title, icon, exec)
        self.model.insertRow(i)
        self.model.setItem(i, item)
        self.ui.lv.setCurrentIndex(self.model.index(i,0))

    def editselected(self):
        i =  self.ui.lv.currentIndex().row()
        if i < 0: return
        if not self.model.item(i).isgroup:
            title, icon, exec = iconedit.iconedit(self.model.item(i).title, self.model.item(i).iconfn, self.model.item(i).exec, self.lang)
            if title == None: return
            self.model.item(i).title = title
            if self.model.item(i).iconfn != icon:
                self.model.item(i).setIcon(iconFromName(icon))
            self.model.item(i).iconfn = icon
            self.model.item(i).exec = exec
            self.model.item(i).setText(title)
        else:
            r, title, withtext = groupedit(self.model.item(i).title, self.model.item(i).withtext, self.lang)
            if not r: return
            self.model.item(i).title = title
            self.model.item(i).withtext = withtext
            self.model.item(i).setText(title)
        #self.model.removeRow(i)

    def delitem(self):
        i =  self.ui.lv.currentIndex().row()
        if i < 0: return
        if self.model.item(i).isgroup:
            reply = QtWidgets.QMessageBox.question(self, self.lang.tr('attention'), self.lang.tr('il_remove_group'), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply != QtWidgets.QMessageBox.Yes: return
            j = i+1
            while j < self.model.rowCount():
                if self.model.item(j).isgroup: break
                self.model.removeRow(j)
            self.model.removeRow(i)

        else:
            reply = QtWidgets.QMessageBox.question(self, self.lang.tr('attention'), self.lang.tr('il_remove'), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply != QtWidgets.QMessageBox.Yes: return
            self.model.removeRow(i)

    def moveitem(self, item, f, t):
        nitem = Item()
        nitem.assign(item)
        self.model.removeRow(f)
        self.model.insertRow(t)
        self.model.setItem(t, nitem)

    def moveupgroup(self, i):
        #Первое найдём начало группы выше
        prevgroup = -1
        for j in range(i-1,-1,-1):
            if self.model.item(j).isgroup:
                prevgroup = j
                break
        if prevgroup < 0:
            return
        #Найдем последний элемент группы
        lastingroup = self.model.rowCount()-1
        for j in range(i+1,self.model.rowCount()):
            if self.model.item(j).groupindex != self.model.item(i).groupindex:
                lastingroup = j-1
                break
        j = prevgroup

        for n in range(i, lastingroup+1):
            self.moveitem(self.model.item(n),n,j)
            j+=1
        self.ui.lv.setCurrentIndex(self.model.index(prevgroup,0))


    def movedowngroup(self, i):
        #Найдем следущую группу
        nextgroup = self.model.rowCount()
        for j in range(i+1,self.model.rowCount()):
            if self.model.item(j).groupindex != self.model.item(i).groupindex:
                nextgroup = j
                break

        if nextgroup > self.model.rowCount()-2:
            return
        self.moveupgroup(nextgroup)




    def moveup(self):
        i =  self.ui.lv.currentIndex().row()
        if i < 2: return
        if self.model.item(i).isgroup:
            self.moveupgroup(i)
            return
        m = i-1
        self.moveitem(self.model.item(i),i,m)
        self.ui.lv.setCurrentIndex(self.model.index(m,0))

    def movedown(self):
        i =  self.ui.lv.currentIndex().row()
        if i > self.model.rowCount()-2: return
        if self.model.item(i).isgroup:
            self.movedowngroup(i)
            return
        m = i+1
        self.moveitem(self.model.item(i),i,m)
        self.ui.lv.setCurrentIndex(self.model.index(m,0))

    def savetosets(self):
        gl = []
        gr = None
        for i in range(self.model.rowCount()):
            if self.model.item(i).isgroup:
                if gr != None: gl.append(gr)
                gr = {'title': self.model.item(i).title, 'withtext': self.model.item(i).withtext, 'items': []}
            elif gr != None:
                item = {'title': self.model.item(i).title,'icon': self.model.item(i).iconfn,'exec': self.model.item(i).exec}
                gr['items'].append(item)

        if gr != None: gl.append(gr)
        self.panel.sets.sets['groups'] = gl


def main():
    app = QtWidgets.QApplication(sys.argv)
    d = IconListDialog(app)
    d.exec()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

