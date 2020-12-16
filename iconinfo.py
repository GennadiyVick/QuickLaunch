#
# class IconInfo 
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
from PyQt5 import QtCore
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QIcon
from PyQt5 import Qt
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QGraphicsPixmapItem
from animate import ScaleAnimate

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
            if not QFile.exists(self.icon):
                icn = QIcon.fromTheme(self.icon)
            else:
                icn = QIcon(self.icon)
            self.item = scene.addPixmap(icn.pixmap(QSize(self.iconsize,self.iconsize)))
            self.item.setTransformationMode(QtCore.Qt.SmoothTransformation)
            self.item.setScale(self.defScale)
            self.item.setPos(QPointF(x,y))
            movedist = (1.0-self.defScale) * self.iconsize / 2
            #self.item.setOffset(QPointF(movedist,movedist))
            #scalestap = (1.0-defScale) / stapcnt;
            #self.item.setScale(self.defScale)
        except Exception:
            self.item = None
            return False
        return True
    def changeIcon(self,icon):
        self.icon = icon
        icn = QIcon(self.icon)
        self.item.setPixmap(icn.pixmap(QSize(self.iconsize,self.iconsize)))

    def ptInIcon(self,xx,yy):
        return xx >= self.x and yy >= self.y and yy <= self.y+self.framesize and xx <= self.x+self.framesize
    def nilitem(self):
        self.item = None
    def setpos(self,xx,yy):
        self.x = xx
        self.y = yy
        self.item.setPos(xx,yy)
        
