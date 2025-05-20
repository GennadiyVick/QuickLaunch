#!/usr/bin/python3
# -*- coding: utf-8 -*-

# The program to manage a panel-type windows where you can drop
# a .desktop extension file to the panel to quickly launch programs or other commands.
# more information read in readme file.
#
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
# 

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel
import sys
import json
import os
from lang import Lang

from quicklaunchwindow import Ui_QuickLaunchPanelsWindow
from panel import Panel
import settings
from server import StreamServer, send


class Application(QtWidgets.QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        self._singular = QtCore.QSharedMemory("SharedMemoryForOnlyOneInstanceOfQuicklaunch", self)

    def lock(self):
        if self._singular.attach(QtCore.QSharedMemory.ReadOnly):
            self._singular.detach()
            return False
        if self._singular.create(1):
            return True
        return False


class QuickLaunchPanelsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QuickLaunchPanelsWindow, self).__init__(None)
        self.ui = Ui_QuickLaunchPanelsWindow()
        self.lang = Lang()
        self.ui.setupUi(self, self.lang)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.canClose = False
        self.configdir = settings.Settings.getConfigDir()
        self.initTray()
        self.app = parent
        self.canClose = False
        self.dialogs = []
        self.shortcuts = {}
        self.panels = []
        self.model = QStandardItemModel(self);
        self.ui.lv.setModel(self.model)
        self.ui.lv.setStyleSheet(
            "QListView {background: #2b2b2b; padding: 4px; border-style: inset; border-width: 1px; border-color: #90404050;border-radius: 10px;}")

        self.ui.lv.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.lv.customContextMenuRequested.connect(self.initContextMenu)
        self.loadpanels()
        self.ui.bEdit.clicked.connect(self.editclick)
        self.ui.bAdd.clicked.connect(self.addclick)
        self.ui.bDel.clicked.connect(self.delclick)
        self.setWindowIcon(QIcon(':/run.png'))
        self.runserver()

    def runserver(self):
        thread = QtCore.QThread()
        self.serv = StreamServer(thread)
        self.serv.onRead.connect(self.doRead)
        self.serv.moveToThread(thread)
        thread.started.connect(self.serv.run)
        thread.start()

    def doRead(self, data):
        # print('do read')
        attr = data.split()
        if len(attr) > 1:
            if attr[0].lower() == '-s':
                for i in range(self.model.rowCount()):
                    s = self.model.data(self.model.index(i, 0))
                    if s.lower() == attr[1].lower():
                        self.show_panel(i)
                        break

    def initContextMenu(self, pos):
        menu = QMenu(self)
        act = QAction(self.lang.tr('show_window'), self)
        act.triggered.connect(self.showdialog)
        menu.addAction(act)

        p = self.mapToGlobal(pos)
        p.setX(p.x() + 1)
        p.setY(p.y() + 1)
        menu.exec_(p)

    def show_panel(self, index):
        if self.panels[index]['visible']:
            self.dialogs[index].hide()
            self.panels[index]['visible'] = False
        else:
            self.show_dialog(self.dialogs[index])
            self.panels[index]['visible'] = True

    def show_dialog(self, dlg):
        dlg.opacity_effect.setOpacity(0.0)
        dlg.show()
        QtCore.QTimer.singleShot(50, dlg.start_show_animate)

    def showdialog(self):
        if self.model.rowCount() == 0: return
        i = self.ui.lv.currentIndex().row()
        self.show_dialog(self.dialogs[i])
        self.panels[i]['visible'] = True

    def loadpanels(self):
        fn = self.configdir / 'panels.json'
        if not os.path.isfile(fn): return
        with open(fn, encoding='utf-8') as f:
            self.panels = json.load(f)
        for info in self.panels:
            item = QtGui.QStandardItem(info['title'])
            self.model.appendRow(item)
            visible = True
            if 'visible' in info:
                visible = info['visible']
            else:
                info['visible'] = True
            self.createdialog(info['filename'], visible)

    def savepanels(self):
        fn = self.configdir / 'panels.json'
        with open(fn, 'w', encoding='utf-8') as f:
            json.dump(self.panels, f, ensure_ascii=False, indent=4)

    def closePanel(self, panel):
        index = -1
        for i in range(len(self.dialogs)):
            if panel == self.dialogs[i]:
                index = i
                break
        if index < 0: return
        self.panels[i]['visible'] = False

    def createdialog(self, filename, visible, title=None):
        dialog = Panel(self, filename, title)
        self.dialogs.append(dialog)
        dialog.onCloseSignal.connect(self.closePanel)
        if visible:
            self.show_dialog(dialog)

    def closeDialogs(self):
        for dialog in self.dialogs:
            dialog.close()
        self.dialogs.clear()

    def doQuit(self):
        self.canClose = True
        if self.app is not None and "Application" in str(type(self.app)):
            self.serv.keep_running = False
            self.closeDialogs()
            self.savepanels()
            self.app.quit()

    def trayclick(self, i_reason):
        if i_reason == 3:  # buttons & Qt.LeftButton:
            for dialog in self.dialogs:
                dialog.activateWindow()

    def closeEvent(self, event):
        if not self.canClose:
            event.ignore()
            self.hide()
        else:
            self.closeDialogs()

    def initTray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(":/run.png"))  #QIcon.fromTheme("preferences-system"))

        show_action = QAction(self.lang.tr("show_list"), self)
        quit_action = QAction(self.lang.tr("quit"), self)
        # hide_action = QAction("Hide",self)

        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.doQuit)
        # hide_action.triggered.connect(self.hide)

        traymenu = QMenu()
        traymenu.addAction(show_action)
        # traymenu.addAction(hide_action)
        traymenu.addAction(quit_action)
        self.tray.setContextMenu(traymenu)
        self.tray.activated.connect(self.trayclick)
        self.tray.show()

    def editclick(self):
        if self.model.rowCount() == 0: return
        i = self.ui.lv.currentIndex().row()
        txt = self.ui.lv.currentIndex().data()
        text, ok = QInputDialog.getText(self, self.lang.tr('panel_caption'), self.lang.tr('enter_panelname'), text=txt)
        if ok and txt != text:
            self.panels[i]['title'] = text
            self.dialogs[i].changeTitle(text)
            self.model.item(i).setText(text)
        self.savepanels()

    def addclick(self):
        text, ok = QInputDialog.getText(self, self.lang.tr('panel_caption'), self.lang.tr('enter_panelname'))
        if ok and len(text) > 1:
            fn = "".join(x for x in text if x.isalnum())
            fn += '.json'
            item = QtGui.QStandardItem(text)
            self.model.appendRow(item)
            self.panels.append({'title': text, 'filename': fn})
            self.createdialog(fn, True, text)

    def delclick(self):
        if self.model.rowCount() == 0: return
        i = self.ui.lv.currentIndex().row()
        reply = QMessageBox.question(self, self.lang.tr("attention"), self.lang.tr("remove_panel"),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes: return
        # panelname = self.panels[i]['title']
        fn = self.configdir / self.panels[i]['filename']
        if os.path.exists(fn): os.remove(fn)
        self.dialogs[i].close()
        self.dialogs.pop(i)
        self.panels.pop(i)
        self.model.removeRow(i)


def main():
    app = Application(sys.argv)
    if not app.lock():
        if len(sys.argv) > 1:
            send('\n'.join(sys.argv[1:]))
        return -42
    app.setQuitOnLastWindowClosed(False)
    main = QuickLaunchPanelsWindow(app)
    app.mainwindow = main
    #main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
