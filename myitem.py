from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsTextItem, QGraphicsSceneHoverEvent,
    QGraphicsItemGroup, QGraphicsPixmapItem, QGraphicsObject, QGraphicsRectItem, QGraphicsDropShadowEffect)
from PyQt5.QtCore import QPoint, QPointF, QSize, QSizeF, QRectF, QObject, QFile, Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QColor, QBrush
from animate import AniStack,ScaleAnimate,OpacityAnimate,MoveAnimate
from os.path import expanduser
import json

class Item():
    def __init__(self, signals = None):
        #self.prnt = prnt
        if signals == None: return
        self.index = 0
        self.anilist = {'scale':AniStack(ScaleAnimate), 'move': AniStack(MoveAnimate)}
        self.visible = True
        self.title = ''
        self.icon = ''
        self.exec = ''
        self.deficonsize = 48
        self.moved = False
        self.mx = 0
        self.my = 0
        self.onHover = None
        self.onClick = None
        self.onMove = None

        if 'hover' in signals:
            self.onHover = signals['hover']
        if 'click' in signals:
            self.onClick = signals['click']
        if 'move' in signals:
            self.onMove = signals['move']

    def changeIcon(self):
        pass

    def addAni(self,animation,start,stop,item = None, maxsteps = 6):
        i = item
        if item == None: i = self
        self.anilist[animation].addAni(i,start,stop, maxsteps)

    def iconFromName(self):
        icn = None
        if not QFile.exists(self.icon):
            icn = QIcon.fromTheme(self.icon)
            if icn.isNull():
                icn = self.findicon()
                if icn == None or icn.isNull():
                    icn = QIcon(":/icon.png")
        else:
            icn = QIcon(self.icon)
        return icn

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

class TItem(QGraphicsTextItem,Item):
    def __init__(self,parent,sinals = {}):
        Item.__init__(self,sinals)
        self.parent = parent
        QGraphicsTextItem.__init__(self)
        self.setAcceptHoverEvents(True)
'''
    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        if self.onHover != None:
            self.onHover.emit(self,True)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        if self.onHover != None:
            self.onHover.emit(self,False)
'''

class RItem(QGraphicsRectItem, Item):
    def __init__(self,parent, signals = {}):
        Item.__init__(self,signals)
        QGraphicsRectItem.__init__(self)
        self.parent = parent

class GItem(QGraphicsPixmapItem,Item):
    def __init__(self, parent, signals, icon,title, exec):
        Item.__init__(self, signals)
        QGraphicsPixmapItem.__init__(self)
        self.parent = parent
        self.sets = self.parent.sets
        self.setAcceptHoverEvents(True)
        self.title = title
        self.icon = icon
        self.exec = exec
        self.deficonsize = parent.deficonsize
        #self.scaled = parent.scaled
        #self.defscale = parent.defscale
        self.setTransformationMode(QtCore.Qt.SmoothTransformation)
        originpoint = parent.deficonsize/2
        self.setTransformOriginPoint(originpoint,originpoint);
        if self.sets.get('panel.shaddow',False):
            eff = QGraphicsDropShadowEffect()
            eff.setBlurRadius(self.sets.get('panel.shaddowgause',6.0))
            eff.setOffset(self.sets.get('panel.shaddowoffsetx',2.0))
            eff.setColor(QColor(self.sets.get('panel.shaddowcolor','#80000000')))
            self.setGraphicsEffect(eff)

        self.changeIcon()

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        if self.onHover != None:
            self.onHover.emit(self,True)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        if self.onHover != None:
            self.onHover.emit(self,False)

    def changeIcon(self):
        icn = self.iconFromName()
        if icn != None:
            pix = icn.pixmap(icn.actualSize(QSize(self.deficonsize, self.deficonsize)))
            self.setPixmap(pix.scaled(self.deficonsize,self.deficonsize,Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        self.canmove = event.button() == Qt.LeftButton
        if not self.canmove: return
        self.mx = event.pos().x()
        self.my = event.pos().y()
        self.moved = False

    def mouseMoveEvent(self, event):
        if not self.canmove: return
        x = event.pos().x()
        y = event.pos().y()
        if self.moved or (abs(x-self.mx) > 10 or abs(y-self.my) > 10):
            self.moved = True
            if self.onMove != None:
                self.onMove.emit(self,event)

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton: return
        if not self.moved:
            if self.onClick != None:
                self.onClick.emit(self)


class GTItem(QGraphicsItemGroup,Item):
    def __init__(self, parent, signals, icon,title, exec):
        Item.__init__(self, signals)
        QGraphicsItemGroup.__init__(self)
        self.parent = parent
        self.sets = parent.sets
        self.anilist['opacity'] = AniStack(OpacityAnimate)
        self.title = title
        self.icon = icon
        self.exec = exec
        self.deficonsize = parent.deficonsize
        self.setAcceptHoverEvents(True)
        self.gitem = QGraphicsPixmapItem()
        self.titem = QGraphicsTextItem()
        texcol = self.sets.get('panel.textcolor','#80000000')
        self.titem.setHtml(f'<div style="color: {texcol}">{title}</div>')
        #self.titem.setDefaultTextColor(QColor('white'))
        self.titem.setOpacity(0.7)
        self.titem.setAcceptHoverEvents(False)
        self.titem.setPos(parent.fsize+4,(parent.fsize-self.titem.boundingRect().height())/2)
        self.addToGroup(self.titem)
        originpoint = parent.deficonsize/2
        self.gitem.setTransformOriginPoint(originpoint,originpoint);
        self.gitem.setTransformationMode(QtCore.Qt.SmoothTransformation)
        '''
        rect = self.boundingRect()
        self.trect = QGraphicsRectItem(rect)
        self.trect.setPen(QColor(self.sets.get('group.titlebordercolor','#238')))
        self.trect.setBrush(QBrush(QColor(self.sets.get('group.titlebgcolor','#222'))))
        self.trect.setPos(0,0)
        self.trect.setVisible(True)
        self.trect.setZValue(-1);
        self.addToGroup(self.trect)
        '''
        if self.sets.get('panel.shaddow',False):
            eff = QGraphicsDropShadowEffect()
            eff.setBlurRadius(self.sets.get('panel.shaddowgause',6.0))
            eff.setOffset(self.sets.get('panel.shaddowoffsetx',2.0))
            eff.setColor(QColor(self.sets.get('panel.shaddowcolor','#80000000')))
            self.setGraphicsEffect(eff)
        self.changeIcon()
        self.addToGroup(self.gitem)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        self.onHover.emit(self,True)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.onHover.emit(self,False)

    def changeIcon(self):
        icn = self.iconFromName()
        if icn != None:
            pix = icn.pixmap(icn.actualSize(QSize(self.deficonsize, self.deficonsize)))
            self.gitem.setPixmap(pix.scaled(self.deficonsize,self.deficonsize,Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        self.canmove = event.button() == Qt.LeftButton
        if not self.canmove: return
        self.mx = event.pos().x()
        self.my = event.pos().y()
        self.moved = False

    def mouseMoveEvent(self, event):
        if not self.canmove: return
        x = event.pos().x()
        y = event.pos().y()
        if ( abs(x-self.mx) > 10 or abs(y-self.my) > 10):
            self.moved = True
            if self.onMove != None:
                self.onMove.emit(self,event)

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton: return
        if not self.moved:
            if self.onClick != None:
                self.onClick.emit(self)
