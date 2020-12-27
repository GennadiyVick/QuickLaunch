#
# class IconInfo 
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
# 

from PyQt5 import QtCore
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QIcon
from PyQt5 import Qt
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QGraphicsPixmapItem
from animate import ScaleAnimate
from os.path import expanduser

class IconInfo:
    def __init__(self, iconsize,scaledsize,framesize):
        self.iconsize = iconsize
        self.scaledSize = scaledsize
        self.framesize = framesize
        self.title = ""
        self.icon = ""
        self.exec = ""
        self.x = 0  #it set in createIconItem and never change
        self.y = 0
        self.item = None #QGraphicsPixmapItem()
        self.defScale = scaledsize / iconsize
        self.anilist = []
        self.lastScale = self.defScale #set last see in animate __init__
        self.lastOffset = 0
        
        
    def getLine(self):
        return self.title+";"+self.icon+";"+self.exec
       
    def createIconItem(self,scene, x, y):
        
        try :
            self.x = x
            self.y = y
            icn = self.iconFromName()
            self.item = scene.addPixmap(icn.pixmap(QSize(self.iconsize,self.iconsize)))
            self.item.setTransformationMode(QtCore.Qt.SmoothTransformation)
            self.item.setScale(self.defScale)
            self.item.setPos(QPointF(x,y))
            movedist = (1.0-self.defScale) * self.iconsize / 2
            #self.item.setOffset(QPointF(movedist,movedist))
            #scalestap = (1.0-defScale) / stapcnt;
            #self.item.setScale(self.defScale)
        except Exception as e:
            self.item = None
            if hasattr(e, 'message'):
                print("ERROR: "+e.message)
            else:
                print(e)
            return False
        return True
    
    def iconFromName(self):
        icn = None
        if not QFile.exists(self.icon):
            icn = QIcon.fromTheme(self.icon)
            if icn.isNull():
                icn = self.findicon()
                if icn == None or icn.isNull():
                    icn = QIcon(":/images/icon.png")
        else:
            icn = QIcon(self.icon)   
        return icn
    
    def changeIcon(self,icon):
        icn = self.iconFromName()
        self.item.setPixmap(icn.pixmap(QSize(self.iconsize,self.iconsize)))
        
    def findicon(self):
        iconname = self.icon
        home = expanduser("~")
        icondirs = [home+"/.local/share/icons/hicolor/48x48/apps/",
                    home+"/.local/share/icons/hicolor/64x64/apps/",
                    "/usr/share/icons/hicolor/scalable/apps/",
                    "/usr/share/icons/hicolor/48x48/apps/",
                    "/usr/share/app-install/icons/",
                    "/usr/share/pixmaps/",
                    "/usr/share/icons/hicolor/48x48/mimetypes/",
                    "/usr/share/icons/hicolor/64x64/mimetypes/",
                    "/usr/share/icons/gnome/48x48/apps/"]
        exts = [".png",".svg"]
        if ".png" in iconname or ".svg" in iconname:
            for icondir in icondirs:
                fn = icondir+iconname
                if QFile.exists(fn): return QIcon(fn)
        else:
            for icondir in icondirs:
                for ext in exts:
                    fn = icondir + iconname + ext
                    if QFile.exists(fn): return QIcon(fn)
        return None;
    

    def ptInIcon(self,xx,yy):
        return xx >= self.x and yy >= self.y and yy <= self.y+self.framesize and xx <= self.x+self.framesize
    def nilitem(self):
        self.item = None
    def setpos(self,xx,yy):
        self.x = xx
        self.y = yy
        self.item.setPos(xx,yy)
        
