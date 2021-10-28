from PyQt5.QtWidgets import (QGraphicsView)
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QDropEvent
from animate import ScrollAnimate

class MyGraphicsView(QGraphicsView):
    onDrop = QtCore.pyqtSignal(QGraphicsView, QDropEvent)

    def __init__(self, parent = None):
        super(MyGraphicsView, self).__init__(parent)
        #self.anilist = []
        self.setStyleSheet("QGraphicsView {border-width: 0px; border-style: none; outline:0px; background: transparent;}")
        self.anitimer = QTimer(self)
        self.anitimer.timeout.connect(self.onAniTimer)
        #self.sr = 64
        self.ani = ScrollAnimate(self.verticalScrollBar())
        self.defstep = 8

    def onAniTimer(self):
        self.ani.doStep()
        if self.ani.finished:
            self.anitimer.stop()

    def wheelEvent(self, event):
        m = self.verticalScrollBar().maximum()
        if m == 0: return
        v = self.verticalScrollBar().value()

        s = -event.angleDelta().y() // 3

        if s > 0:
            if v >= m: return
            if v + s > m: s = m-v
            self.ani.step = self.defstep
        else:
            if v <= 0: return
            if v + s < 0: s = -v
            self.ani.step = -self.defstep

        if self.ani.finished:
            self.ani.pos = v
            self.ani.lpos = v+s
        else:
            self.ani.lpos += s

        if self.ani.lpos > m: self.ani.lpos = m
        elif self.ani.lpos < 0: self.ani.lpos = 0

        self.ani.finished = False
        if not self.anitimer.isActive(): self.anitimer.start(30)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else: event.ignore()
        #print('dragEnter',event.pos())

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            #event.setDropAction(Qt.CopyAction)
            event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        self.onDrop.emit(self,event)



