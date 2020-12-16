#!/usr/bin/python3
#
# The program shows a pane-type window where you can move files with 
# the .desktop extension to quickly launch programs or other commands.
# The program takes the name of the panel as an argument, by default "Programms"
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
# some else...
# I bag your pardon for russian documentation of functions,
# if you need you can translate it with google

import sys
import os
#import atexit
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFile

import images #imageresources
import wnd #mainwindow class
from mygraphicsview import MyGraphicsView


class PanelWindow(QtWidgets.QWidget):
    #Главное окно программы
    def __init__(self, qApp, title = "Programs"):
        """Функция создания главного окна, здесь создаём
            графический интерфейс с MyLabel основанный на QLabel в качестве заголовка
            и MyGraphicsView созданный на основе QGraphicsView
            для отрисовки значков. Вся логика программы находится
            в классе MyGraphicsView.
            Окно не имеет обычного заголовка и рамок.
            Программа принимает в качестве аргумента наименование
            панели, по умолчанию 'Programms'"""
        super(PanelWindow, self).__init__()
        self.ui = wnd.Ui_PanelWindow() #создаём простой объект ui для 
        self.ui.setupUi(self) #инициализируем окно, создаём компоненты и пр.
        self.qApp = qApp
        self.setWindowTitle(title)
        
        if __name__ == '__main__' and len(sys.argv)>1: #проверяем компоненты
            self.title = sys.argv[1]
        else:
            self.title = title

        #self.ui.ltitle.customContextMenuRequested.connect(self.openContextMenu)
        self.ui.ltitle.setText(self.title)

        set = QSettings("QuickLaunch", "config")
        self.linkPath = os.path.dirname(set.fileName())
        left = int(set.value(self.title+"/Pos/Left","-1"))
        top = int(set.value(self.title+"/Pos/Top","-1"))
        self.ui.centralwidget.setStyleSheet(set.value(self.title+"/style",self.ui.centralwidget.styleSheet()))

        self.listFilename = set.value(self.title+"/Filename","")
        if self.listFilename == "" or not QFile.exists(self.listFilename):
            self.listFilename = self.linkPath +"/"+ self.title + ".lst"
        #==============
        self.mx = -1
        self.my = -1
        #================================================    
        self.scn = QGraphicsScene(self)
        self.scn.setSceneRect(0,0, self.width()-6, self.height()-self.ui.ltitle.height()-6)
        self.gv = MyGraphicsView(self,self.scn,self.listFilename,self.title)
        self.gv.setObjectName("gv")
        self.gv.setStyleSheet("border-width: 0px; border-style: none; outline:0px;")
        self.ui.verticalLayout.addWidget(self.gv)
        self.gv.setRenderHint(QPainter.Antialiasing);
        self.gv.setScene(self.scn)
        self.gv.show()

        self.ui.ltitle.onMousePress.connect(self.mousePress)
        self.ui.ltitle.onMouseMove.connect(self.mouseMove)
        if left > 0:
            if top < 0: top = 1
            self.move(left,top)
        else:
            self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.ps = self.pos()
        #atexit.register(self.onClose)

    def changeTitle(self,newtitle):
        set = QSettings("QuickLaunch", "config")
        set.remove(self.title)
        self.title = newtitle
        self.listFilename = self.linkPath +"/"+ self.title + ".lst"
        if os.path.exists(self.gv.listfn):
            os.remove(self.gv.listfn)
        self.gv.listfn = self.listFilename
        self.gv.ilist.saveToFile(self.listFilename)
        self.gv.paneltitle = self.title
        self.ui.ltitle.setText(self.title)
        
        self.saveConfig()
    
    def saveConfig(self):
        set = QSettings("QuickLaunch", "config")
        p = self.pos()
        set.setValue(self.title+"/Pos/Left",p.x())
        set.setValue(self.title+"/Pos/Top",p.y())
        set.setValue(self.title+"/Filename",self.listFilename)
        set.setValue(self.title+"/style",self.ui.centralwidget.styleSheet())        
        


    def closeEvent(self,event):
        """Событие выхода завершения работы приложения"""
        self.saveConfig()
 

    def mousePress(self,event):
        """Событие нажатия мыши на MyLabel главного окна,
           выступающем в роли заголовка окна,
           в данной функции  переменным присваивается глобальная
           позиция мыши и позиция окна, для того, чтобы при
           перемещении мыши вызывать перемещение главного окна.
           Присоединение (connect) смотрите в функции __init__
           главного окна"""
        self.mx = event.globalPos().x()
        self.my = event.globalPos().y()
        self.ps = self.pos()

    def mouseMove(self,event):
        """Событие перемещения мыши на MyLabel главного окна,
           выступающем в роли заголовка окна,
           в данной функции перемещаем главное окно по экрану.
           Для более полного понимания можете глянуть документацию
           к функции mousePress"""
        x = event.globalPos().x()-self.mx
        y = event.globalPos().y()-self.my
        self.move(self.ps.x()+x,self.ps.y()+y)
    
    def openContextMenu(self, pos):
        """Данная функция вызывает контекстое меню,
            в данный момент она не работает, не вызывается"""
        menu = QMenu()
        menu.setStyleSheet("background: #fff")
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.sender().mapToGlobal(pos))
        if action == quitAction:
            self.qApp.quit()
            
    def closewnd(self):
        if __name__ == '__main__':
            qApp.quit()
        else:
            self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    panelWindow = PanelWindow(app)
    panelWindow.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

