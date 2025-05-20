#
# base  window class / used only in panelwindow class /
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
#

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication
from mywidget import MyWidget
from mylabel import MyLabel


class Ui_window(QtCore.QObject):
    onMovedSignal = QtCore.pyqtSignal()

    def setupUi(self, window, width = 300, height = 300):
        self.window = window
        window.setObjectName("window")
        window.resize(width, height)
        window.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        window.setAttribute(Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {\n"
            "background: #90202020;\n"
            "border-style: inset;\n"
            "border-width: 1px;\n"
            "border-color: #a0404050;\n"
            "border-radius: 10px;}")
        self.centralwidget.setObjectName("centralwidget")
        if window.__class__.__base__.__name__ == 'QMainWindow':
            window.setCentralWidget(self.centralwidget)
        else:
            self.windowLayout = QtWidgets.QVBoxLayout(self.window)
            self.windowLayout.setContentsMargins(0, 0, 0, 0)
            self.windowLayout.setSpacing(0)
            self.windowLayout.setObjectName("windowLayout")
            self.windowLayout.addWidget(self.centralwidget)

        self.mainlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.mainlayout.setObjectName("mainlayout")
        self.wcontent = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.wcontent.sizePolicy().hasHeightForWidth())
        self.wcontent.setSizePolicy(sizePolicy)
        self.wcontent.setObjectName("wcontent")
        self.contentlayout = QtWidgets.QHBoxLayout(self.wcontent)
        self.contentlayout.setContentsMargins(0, 0, 0, 0)
        self.contentlayout.setSpacing(0)
        self.contentlayout.setObjectName("contentlayout")
        self.wcenter = QtWidgets.QWidget(self.wcontent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wcenter.sizePolicy().hasHeightForWidth())
        self.wcenter.setSizePolicy(sizePolicy)
        self.wcenter.setMinimumSize(QtCore.QSize(1, 1))
        self.wcenter.setObjectName("wcenter")
        self.centerLayout = QtWidgets.QVBoxLayout(self.wcenter)
        self.centerLayout.setContentsMargins(4, 0, 0, 0)
        self.centerLayout.setSpacing(0)
        self.centerLayout.setObjectName("centerLayout")
        self.ltitle = MyLabel(self.wcenter)
        self.ltitle.setAlignment(QtCore.Qt.AlignCenter)
        self.ltitle.setObjectName("ltitle")
        self.ltitle.onMouseMove.connect(self.ltitleMouseMove)
        self.ltitle.onMouseRelease.connect(self.ltitleMouseRelease)
        self.ltitle.onMousePress.connect(self.ltitleMousePress)
        self.ltitle.setStyleSheet('padding-top :6px')
        self.centerLayout.addWidget(self.ltitle)
        #self.graphicsView = QtWidgets.QGraphicsView(self.wcenter)
        #self.graphicsView.setObjectName("graphicsView")
        #self.centerLayout.addWidget(self.graphicsView)
        self.contentlayout.addWidget(self.wcenter)
        self.wrborder = MyWidget(self.wcontent)
        self.wrborder.onMouseMove.connect(self.wrborderMouseMove)
        self.wrborder.onMouseRelease.connect(self.wrborderMouseRelease)
        self.wrborder.onMousePress.connect(self.wrborderMousePress)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wrborder.sizePolicy().hasHeightForWidth())
        self.wrborder.setSizePolicy(sizePolicy)
        self.wrborder.setMinimumSize(QtCore.QSize(6, 0))
        self.wrborder.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.wrborder.setStyleSheet("")
        self.wrborder.setObjectName("wrborder")
        self.contentlayout.addWidget(self.wrborder)
        self.mainlayout.addWidget(self.wcontent)
        self.wbottom = MyWidget(self.centralwidget)
        self.wbottom.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.wbottom.setMouseTracking(True)
        self.wbottom.setObjectName("wbottom")
        self.wbottom.onMouseMove.connect(self.wbottomMouseMove)
        self.wbottom.onMouseRelease.connect(self.wbottomMouseRelease)
        self.wbottom.onMousePress.connect(self.wbottomMousePress)

        self.bottomLayout = QtWidgets.QHBoxLayout(self.wbottom)
        self.bottomLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomLayout.setSpacing(0)
        self.bottomLayout.setObjectName("bottomLayout")
        spacerItem = QtWidgets.QSpacerItem(471, 6, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottomLayout.addItem(spacerItem)
        self.lconner = MyLabel(self.wbottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lconner.sizePolicy().hasHeightForWidth())
        self.lconner.setSizePolicy(sizePolicy)
        self.lconner.setMinimumSize(QtCore.QSize(6, 6))
        self.lconner.setMaximumSize(QtCore.QSize(6, 6))
        self.lconner.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        self.lconner.setMouseTracking(True)
        self.lconner.setText("")
        self.lconner.setObjectName("lconner")
        self.lconner.onMouseMove.connect(self.lconnerMouseMove)
        self.lconner.onMouseRelease.connect(self.lconnerMouseRelease)
        self.lconner.onMousePress.connect(self.lconnerMousePress)
        self.bottomLayout.addWidget(self.lconner)
        self.mainlayout.addWidget(self.wbottom)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)
        self.window.move(10,10)
        #self.window.move(QApplication.desktop().screen().rect().center() - self.window.rect().center())

    def onpress(self, event):
        print('on press')

    def wrborderMousePress(self,event):
        self.w = self.window.width()

    def wrborderMouseMove(self, event):
        w = event.globalX()-self.wrborder.mx+self.w
        g = self.window.geometry()
        g.setWidth(w)
        self.window.setGeometry(g)

    def wrborderMouseRelease(self, event):
        self.window.onResizeSignal.emit()

    def wbottomMousePress(self,event):
        self.h = self.window.height()

    def wbottomMouseMove(self, event):
        h = event.globalY()-self.wbottom.my+self.h
        g = self.window.geometry()
        g.setHeight(h)
        self.window.setGeometry(g)

    def wbottomMouseRelease(self, event):
        self.window.onResizeSignal.emit()

    def lconnerMousePress(self,event):
        self.h = self.window.height()
        self.w = self.window.width()

    def lconnerMouseMove(self, event):
        h = event.globalY()-self.lconner.my+self.h
        w = event.globalX()-self.lconner.mx+self.w
        g = self.window.geometry()
        g.setHeight(h)
        g.setWidth(w)
        self.window.setGeometry(g)

    def lconnerMouseRelease(self, event):
        self.window.onResizeSignal.emit()

    def ltitleMousePress(self,event):
        self.l = self.window.pos().x()
        self.t = self.window.pos().y()

    def ltitleMouseMove(self, event):
        t = event.globalY()-self.ltitle.my+self.t
        l = event.globalX()-self.ltitle.mx+self.l
        w = self.window.width()
        h = self.window.height()
        dist = 2
        sdist = 20
        for d in self.window.mainwindow.dialogs:
            if not d.isVisible(): continue
            x = d.pos().x()
            y = d.pos().y()
            dw = d.width()
            dh = d.height()
            if t > y-h+dist and  t < y + dh - dist:
                if l > x - w - sdist and l <  x - w + sdist:
                    l = x - w - dist
                    if t > y - sdist and t < y+ sdist: t = y
                    break
                elif l > x + dw - sdist and l < x + dw + sdist:
                    l = x + dw + dist
                    if t > y - sdist and t < y+ sdist: t = y
                    break
            elif l > x-w+dist and l < x+dw-dist:
                if t > y - h - sdist and t < y - h + sdist:
                    t = y - h - dist
                    if l > x - sdist and l < x + sdist: l = x
                    break
                elif t > y + dh - sdist and t < y + sdist + dh:
                    t = y + dh + dist
                    if l > x - sdist and l < x + sdist: l = x
                    break
        self.window.move(l,t)

    def ltitleMouseRelease(self, event):
        pass
        #self.window.onMovedSignal.emit()

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Form"))
        self.ltitle.setText(_translate("window", "UnTitled"))

