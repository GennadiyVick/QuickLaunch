#
# class MyGraphicsView class based QGraphicsView 
# All program logic is in this class
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
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTextStream
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QMimeData
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QDrag

from iconlist import IconList
import images
from iconinfo import IconInfo
from animate import Animate, ScaleAnimate
from iconeditwnd import IconEditWindow
from desktopparse import DesktopParse
from styleedit import StyleEditWindow

class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent, scene , dir, title):
        super().__init__(parent)
        self.defaultIconSize = 32
        self.defaultIconScaledSize = 48
        self.defaultIconFrameSize = 38
        self.colcnt = scene.width() // self.defaultIconFrameSize;
        self.listfn = dir
        self.mpos = QPointF()
        self.mx = 0
        self.my = 0
        self.scn = scene
        self.ilist = IconList(self)
        self.changedtitle = False
        self.mouseInItem = -1
        self.movemouseItem  = -1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.mltimer = QTimer(self)
        self.mltimer.timeout.connect(self.onMlTimer)
        self.mltimer.setSingleShot(True)
        self.canmovewindow = True
        self.menu = QMenu(self)
        self.prnt = parent
        self.anilist = []
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.paneltitle = title
        self.mouseleavecheck = False
        if (len(self.listfn) > 0 and  QFile.exists(self.listfn)) :
            self.ilist.loadFromFile(self.listfn,scene)
            #set window height 
        #self.initContextMenu()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.initContextMenu)
        self.setHorizontalScrollBarPolicy (Qt.ScrollBarAlwaysOff );
        self.setVerticalScrollBarPolicy (Qt.ScrollBarAlwaysOff );
        self.itemDrag = -1

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else: event.ignore()
        #if event.mimeData().hasFormat("text/plain"):
        #    event.acceptProposedAction()
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else: event.ignore()
        #event.acceptProposedAction()
    #def dragLeaveEvent(self, event):
        #global window
    #    drag = QDrag(self)
    #    data = QMimeData()
    #    data.setData("text/plain", "")

#        files = []
        #files.append(QUrl.fromLocalFile("/home/genius/yandexdisk/python/GuiPy/gui.ui")
 #       files.append(QUrl.fromLocalFile("/home/genius/yandexdisk/python/GuiPy/gui.ui"))
  #      data.setUrls(files)
  #      drag.setMimeData(data)
  #      drag.exec_(QtCore.Qt.CopyAction) 
    
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                fn = str(url.toLocalFile())
                title,icon,exec = DesktopParse().parse(self.prnt, fn)
                if title != "" and icon != "" and exec != "":
                    self.ilist.addItem(icon,exec,title)
                #print(title,icon,exec)
        #url = QUrl(event.mimeData().text())
        #path = url.path().simplified()
        #title,icon,exec = DesktopParse().parse(self.prnt, path)
        #if title == "" or exec == "" or icon == "": return
        
        
    
    def initContextMenu(self, pos):
        menu = QMenu(self.prnt)
        menu.setStyleSheet("background: #222")

        act = QAction(QIcon(":/images/css.svg"),"Стиль окна",self.prnt)
        menu.addAction(act)
        act.triggered.connect(self.stylebtn)

        menu.addSeparator()
        act = QAction(QIcon(":/images/add.png"),"Добавить кнопку",self.prnt)
        menu.addAction(act)
        act.triggered.connect(self.addbtn)
        
        act = QAction(QIcon(":/images/delete.png"),"Удалить кнопку",self.prnt)
        menu.addAction(act)
        act.triggered.connect(self.delbtn)
        
        act = QAction(QIcon(":/images/edit.png"),"Изменить кнопку",self.prnt)
        menu.addAction(act)
        act.triggered.connect(self.editbtn)
        
        menu.addSeparator()
        
        act = QAction(QIcon(":/images/exit24.png"),"Выход",self.prnt)
        act.triggered.connect(self.exitbtn);
        menu.addAction(act)
        p = self.mapToGlobal(pos)
        p.setX(p.x()+1)
        p.setY(p.y()+1)
        menu.exec_(p)
        
        #super().setContextMenu(menu)
    
    
    def onTimer(self):
        stop = True
        for iconinfo in self.ilist:
            if len(iconinfo.anilist) > 0:
                a = iconinfo.anilist[0]
                a.doStep()
                if a.finished:
                    iconinfo.anilist.pop(0)
            if len(iconinfo.anilist) > 0:
                stop = False
        if stop: self.timer.stop()
                
    def onMlTimer(self):
        self.timer.stop()
        self.prnt.ui.ltitle.setText(self.prnt.title)
        for iconinfo in self.ilist:
            if iconinfo.item.scale() != iconinfo.defScale:
                s = self.defaultIconSize/self.defaultIconScaledSize
                a = ScaleAnimate(iconinfo,s)
                iconinfo.anilist.append(a)
                if not self.timer.isActive(): self.timer.start(30)
                            
    
    def addbtn(self):
        ie = IconEditWindow()
        if ie.exec_() == 1:
            title = ie.ui.eTitle.text()
            icon = ie.ui.eIcon.text()
            exec = ie.ui.eExec.text()
            if len(exec) > 1 and len(icon) > 1:
                self.ilist.addItem(icon,exec,title)
        
        #self.ilist.addItem(":/images/icon.png","asdf","some Icon")
    
    def delbtn(self):
        if self.mouseInItem >= 0 and self.mouseInItem < self.ilist.cnt()-1:
            for j in range(self.ilist.cnt()-1, self.mouseInItem,-1):
                i1 = self.ilist[j]
                i2 = self.ilist[j-1]
                i1.item.setPos(i2.item.pos())
                i1.x = i2.x
                i1.y = i2.y

        self.prnt.scn.removeItem(self.ilist[self.mouseInItem].item)
        self.ilist.pop(self.mouseInItem);
        self.ilist.saveToFile(self.listfn)
        #list.saveToFile(self.listfn)
    
    def editbtn(self):
        if self.mouseInItem < 0 or self.mouseInItem >= self.ilist.cnt(): return
        i = self.ilist[self.mouseInItem]
        ie = IconEditWindow()
        ie.ui.eTitle.setText(i.title)
        ie.ui.eExec.setText(i.exec)
        ie.ui.eIcon.setText(i.icon)
        if ie.exec_() == 1:
            title = ie.ui.eTitle.text()
            icon = ie.ui.eIcon.text()
            exec = ie.ui.eExec.text()
            if len(exec) > 1 and len(icon) > 1:
                i.exec = exec
                i.title = title
                i.changeIcon(icon)
                self.ilist.saveToFile(self.listfn)
                
    
    def exitbtn(self):
        self.prnt.closewnd()

    def stylebtn(self):
        se = StyleEditWindow(self.prnt)
        se.ui.pEdit.setPlainText(self.prnt.ui.centralwidget.styleSheet())
        se.ui.centralwidget.setStyleSheet(self.prnt.ui.centralwidget.styleSheet())
        if se.exec_() == 1:
            self.prnt.ui.centralwidget.setStyleSheet(se.ui.pEdit.toPlainText())
    
    
    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton: return
        if self.mouseInItem >= 0 and self.mouseInItem < self.ilist.cnt():
            iconinfo = self.ilist[self.mouseInItem]
            ls = iconinfo.lastScale
            iconinfo.anilist.append(ScaleAnimate(iconinfo,1.4,4))
            iconinfo.anilist.append(ScaleAnimate(iconinfo,0.7,4))
            iconinfo.anilist.append(ScaleAnimate(iconinfo,ls,9))
            if not self.timer.isActive(): self.timer.start(30)
            proc = QProcess()
            proc.startDetached(iconinfo.exec)

    def mouseReleaseEvent(self, event):
        pass
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.itemDrag < 0:
                x = int((event.localPos().x()-8) / self.defaultIconFrameSize)
                y = int((event.localPos().y()-8) / self.defaultIconFrameSize)
                i = int(y * self.colcnt + x)
                cnt = self.ilist.cnt()
                if i < 0 or i >= cnt or x > self.colcnt-1: i = -1
                #if i >=0: self.itemDrag = i
                    
            #mimeData = QMimeData()
            #mimeData.setText("asdfasdf")
            #lst = []
            #lst.append(QUrl("/home/genius/yandexdisk/python/GuiPy/point.py"));
            #mimeData.setUrls(lst)
            #dragPixmap = self.grab()
            #drag = QDrag(self)
            #drag.setMimeData(mimeData)
            #drag.setPixmap(dragPixmap)
            #drag.setHotSpot(event.pos())
            #drag.exec_(Qt.MoveAction | Qt.CopyAction)
            #drag.exec_(Qt.CopyAction)

        if self.ilist.cnt() > 0 and event.buttons() == Qt.NoButton:
            x = int((event.localPos().x()-8) / self.defaultIconFrameSize)
            y = int((event.localPos().y()-8) / self.defaultIconFrameSize)
            i = int(y * self.colcnt + x)
            cnt = self.ilist.cnt()
            if i < 0 or i >= cnt or x > self.colcnt-1: i = -1

            if i != self.mouseInItem:
                if self.mouseInItem >= 0 and self.mouseInItem < cnt:
                    iconinfo = self.ilist[self.mouseInItem]
                    s = self.defaultIconSize/self.defaultIconScaledSize
                    a = ScaleAnimate(iconinfo,s)
                    iconinfo.anilist.append(a)
                    if not self.timer.isActive(): self.timer.start(30)
                self.mouseInItem = i    
                if i < 0 or i >= cnt:
                    self.mouseInItem = -1
                    self.prnt.ui.ltitle.setText(self.prnt.title)
                    return    
                iconinfo = self.ilist[self.mouseInItem]
                self.prnt.ui.ltitle.setText(iconinfo.title)
                a = ScaleAnimate(iconinfo,1.0)
                iconinfo.anilist.append(a)
                if not self.timer.isActive(): self.timer.start(30)
                self.mltimer.start(2000)
            
   
