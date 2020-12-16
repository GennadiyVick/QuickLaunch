#!/usr/bin/python3
# QuickLaunchPanels Program to manage of panels of quick launch
# you can show , add, rename and delete a panel. Programm use tray icon with context menu for show window and close.
#
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
 
from PyQt5 import QtGui, QtCore,QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSystemTrayIcon, \
    QAction, QStyle, QMenu, QInputDialog, QMessageBox
from PyQt5.QtCore import QSize,QRect, Qt, QSettings
from PyQt5.QtGui import QIcon, QStandardItemModel
import sys
import os

from quicklaunchpanels_gui import Ui_QuickLaunchPanelsWindow
from quicklaunch import PanelWindow
 
 

 
class QuickLaunchPanelsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QuickLaunchPanelsWindow, self).__init__(None)
        self.ui = Ui_QuickLaunchPanelsWindow()
        self.ui.setupUi(self)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.canClose = False
        self.initTray()
        self.app = parent
        self.dialogs = []
        #self.fn = os.path.dirname(os.path.abspath(__file__))
        #self.fn += "/panels.lst"
        self.panels = []
        self.model = QStandardItemModel(self);
        self.ui.lv.setModel(self.model)
        self.ui.lv.setStyleSheet("QListView::item {font-size: 200%; color: #fff; padding: 5px 5px 5px 1px;}")
        self.ui.lv.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.lv.customContextMenuRequested.connect(self.initContextMenu)        
        self.loadpanels()
        self.ui.bEdit.clicked.connect(self.editclick)
        self.ui.bAdd.clicked.connect(self.addclick)
        self.ui.bDel.clicked.connect(self.delclick)
        self.setWindowIcon(QIcon(':/images/run.png'))
        

    def initContextMenu(self, pos):
        menu = QMenu(self)
        #menu.setStyleSheet("background: #222")
        act = QAction("Показать окно",self)
        act.triggered.connect(self.showdialog);
        menu.addAction(act)
        p = self.mapToGlobal(pos)
        p.setX(p.x()+1)
        p.setY(p.y()+1)
        menu.exec_(p)

    def showdialog(self):
        if self.model.rowCount() == 0: return
        i = self.ui.lv.currentIndex().row()
        self.dialogs[i].show()
               

    def loadpanels(self):
        set = QSettings("QuickLaunch", "config")
        self.panels = set.childGroups()
        if len(self.panels) == 0:
            self.panels = ["Programms"]
        for panelnm in self.panels:
            item = QtGui.QStandardItem(panelnm)
            self.model.appendRow(item)
            self.createdialog(panelnm)
            
    def createdialog(self,panelname):
        dialog = PanelWindow(self.app,panelname) 
        self.dialogs.append(dialog)
        dialog.show()
        
    def closeDialogs(self):
        for dialog in self.dialogs:
            dialog.close()
        self.dialogs.clear()
            
    def doQuit(self):
        self.canClose = True
        if self.app != None and "QApplication" in str(type(self.app)):
            self.closeDialogs()
            self.app.quit()
        
        
    def trayclick(self, i_reason):
        if i_reason == 3: # buttons & Qt.LeftButton:
            for dialog in self.dialogs:
                dialog.activateWindow()

            
        #dialog = MainWindow(self) #Second(self)
        #self.dialogs.append(dialog)
        #dialog.show()
    
    def closeEvent(self,event):
        if not self.canClose:
            event.ignore()
            self.hide()
        else: self.closeDialogs()

    
    def initTray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(":/images/run.png")) #QIcon.fromTheme("preferences-system"))
        
        show_action = QAction("Показать список",self)
        quit_action = QAction("Выход",self)
        #hide_action = QAction("Hide",self)
        
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.doQuit)
        #hide_action.triggered.connect(self.hide)
        
        traymenu = QMenu()
        traymenu.addAction(show_action)
        #traymenu.addAction(hide_action)
        traymenu.addAction(quit_action)
        self.tray.setContextMenu(traymenu)
        self.tray.activated.connect(self.trayclick)
        self.tray.show()

    def editclick(self):
        if self.model.rowCount() == 0: return
        i = self.ui.lv.currentIndex().row()
        txt = self.ui.lv.currentIndex().data()
        text, ok = QInputDialog.getText(self, 'Заголовок панели', 'Введите имя панели:',text=txt)
        if ok and txt != text:
            self.panels[i] = text
            self.dialogs[i].changeTitle(text)


    def addclick(self):
        text, ok = QInputDialog.getText(self, 'Заголовок панели', 'Введите имя панели:')
        if ok and len(text) > 1:
            item = QtGui.QStandardItem(text)
            self.model.appendRow(item)
            self.panels.append(text)
            self.createdialog(text)
            
    def delclick(self):
        if self.model.rowCount() == 0: return
        i = self.ui.lv.currentIndex().row()
        reply = QMessageBox.question(self, "Внимание!!", "Удалить панель со значками?", QMessageBox.Yes|QMessageBox.No)
        if reply != QMessageBox.Yes: return
        set = QSettings("QuickLaunch", "config")
        panelname = self.panels[i]
        fn = set.value(panelname+"/Filename","")
        if os.path.exists(fn): os.remove(fn)
        self.dialogs[i].close()
        self.dialogs.pop(i)
        self.panels.pop(i)
        self.model.removeRow(i)
        set.remove(panelname)        

 
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    main = QuickLaunchPanelsWindow(app)
    #main.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
