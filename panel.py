#
# Panel of icons for quick launch
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
#
import sys
import os
import images
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QWidget,QMenu,QAction, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsSceneMouseEvent)
from PyQt5.QtCore import Qt, QTimer, QSize, QPointF, QUrl #QSize,QRect,
from PyQt5.QtGui import QIcon, QPainter
from panelwindow import Ui_panelwindow
from settingsdialog import SettingsDialog
from iconlistedit import IconListDialog
from settings import Settings
from itemlist import GroupList
from myitem import Item
import desktopparse
import iconedit
import groupedit
import win


class Panel(QWidget):
    onHoverSignal = QtCore.pyqtSignal(QGraphicsItem, bool)
    onClickSignal = QtCore.pyqtSignal(Item)
    onResizeSignal = QtCore.pyqtSignal()
    onMovedSignal = QtCore.pyqtSignal(Item, QGraphicsSceneMouseEvent)
    onCloseSignal = QtCore.pyqtSignal(QWidget)
    cdir = Settings.getConfigDir()

    def __init__(self, mainwindow, setfn = 'Programms.json', title = None):
        super(Panel, self).__init__()
        if not os.path.isdir(self.cdir):
            os.makedirs(self.cdir)
        self.mainwindow = mainwindow
        self.qApp = mainwindow.app
        self.lang = mainwindow.lang
        self.ui = Ui_panelwindow()
        self.ui.setupUi(self)
        self.ui.ltitle.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.ltitle.customContextMenuRequested.connect(self.titleContextMenu)
        self.sets = Settings(self.cdir / setfn)
        if title is not None:
            self.sets.set('title', title)
        if ('left' in self.sets.sets) and ('top' in self.sets.sets):
            self.move(self.sets.sets['left'],self.sets.sets['top'])
        if ('width' in self.sets.sets) and ('height' in self.sets.sets):
            self.resize(QSize(self.sets.sets['width'],self.sets.sets['height']))
        self.onResizeSignal.connect(self.onResize)
        self.onMovedSignal.connect(self.onMoved)
        self.onHoverSignal.connect(self.onHover)
        self.onClickSignal.connect(self.onClick)
        self.signals = {'hover':self.onHoverSignal, 'click':self.onClickSignal,'move':self.onMovedSignal}
        self.scene = QGraphicsScene(self)
        self.gv = self.ui.gv
        self.gv.setRenderHint(QPainter.Antialiasing);
        self.gv.setScene(self.scene)
        self.gv.onDrop.connect(self.dropEvent)
        self.gv.setHorizontalScrollBarPolicy (Qt.ScrollBarAlwaysOff )
        self.gv.show()
        self.gv.setContextMenuPolicy(Qt.CustomContextMenu)
        self.gv.customContextMenuRequested.connect(self.gvContextMenu)
        self.glist = GroupList(self.scene,self.sets,self.gv)
        self.focusitem = -1
        self.anitimer = QTimer(self)
        self.anitimer.timeout.connect(self.onAniTimer)
        self.removetimer = QTimer(self)
        self.removetimer.timeout.connect(self.onRemoveTimer)
        self.removetimer.setInterval(5000)
        self.applysets()
        self.chtltimer = QTimer(self)
        self.chtltimer.timeout.connect(self.doChangeTitle)
        self.savetimer = QTimer(self)
        self.savetimer.timeout.connect(self.savetimertimer)
        self.savetimer.setInterval(60000)
        self.changetitle = None
        self.tempflist = []
        self.anisteps = self.sets.get('panel.anisteps',6)
        self.anistepsclick = self.sets.get('panel.anistepsclick',4)
        self.mainwindow.selfdrag = False


    def resizetimer(self):
        QtCore.QTimer.singleShot(50, self.onResize)

    def savetimertimer(self):
        self.savetimer.stop()
        self.savesettings()

    def savesettings(self):
        self.sets.sets['left'] = self.pos().x()
        self.sets.sets['top'] = self.pos().y()
        self.sets.sets['width'] = self.size().width()
        self.sets.sets['height'] = self.size().height()
        self.sets.sets['title'] = self.ui.ltitle.text();
        self.glist.savetosets()
        self.sets.save()
        for tfn in self.tempflist:
            try:
                os.remove(tfn)
            except:
                pass

    def closeEvent(self, event):
        self.savesettings()

        if __name__ == '__main__':
            self.qApp.quit()

    def titleContextMenu(self, pos):
        menu = QMenu()
        menu.setStyleSheet('background: '+self.sets.get('window.menubgcolor','#222')+'; color: '+self.sets.get('window.menucolor','#fff')+'; padding: 6px;')
        iconlistAction = menu.addAction(self.lang.tr("icon_list"))
        iconlistAction.setIcon(QIcon(':/iconlist.png'))
        settingsAction = menu.addAction(self.lang.tr("settings"))
        settingsAction.setIcon(QIcon(':/set.png'))
        menu.addSeparator()
        addgroupAction = menu.addAction(self.lang.tr('add_group'))
        addgroupAction.setIcon(QIcon(':/addgroup.png'))
        menu.addSeparator()
        quitAction = menu.addAction(self.lang.tr('quit'))
        quitAction.setIcon(QIcon(':/quit.png'))
        action = menu.exec_(self.sender().mapToGlobal(pos))
        if action == quitAction:
            self.onCloseSignal.emit(self)
            self.close()
        elif action == settingsAction:
            dialog = SettingsDialog(self.sets,self.lang, self)
            dialog.loadfromsets()
            if dialog.exec() == 1:
                dialog.savetosets()
                self.sets.save()
                self.applysets()
        elif action == addgroupAction:
            shladd, title, withtext = groupedit.groupAdd(self.lang,self.sets.get('panel.withtext',False))
            if shladd:
                self.glist.addList(title, (0,0),withtext)
                self.savetimer.stop()
                self.savetimer.start()
        elif action == iconlistAction:
            dialog = IconListDialog(self, self.lang)
            if dialog.exec() == 1:
                dialog.savetosets()
                self.glist.loadfromsets(self.signals)
                self.setSceneRect()

    def startfile(self,filename):
        try:
            os.startfile(filename)
        except:
            subprocess.Popen(['xdg-open', filename])

    def gvContextMenu(self, pos):
        if len(self.glist) == 0:
            self.titleContextMenu(pos)
            return
        if self.focusitem < 0:
            for i in range(len(self.glist)-1,-1,-1):
                if pos.y() > self.glist[i].startpos[1]:
                    self.groupContextMenu(pos,self.glist[i])
                    return
            self.titleContextMenu(pos)
            return
        if self.groupitem < 0 or self.groupitem >= len(self.glist): return
        if self.focusitem < 0 or self.focusitem >= len(self.glist[self.groupitem]): return;
        menu = QMenu()
        menu.setStyleSheet('background: '+self.sets.get('window.menubgcolor','#222')+'; color: '+self.sets.get('window.menucolor','#fff')+'; padding: 6px;')
        changeAction = menu.addAction(self.lang.tr("change"))
        changeAction.setIcon(QIcon(':/edit.png'))
        menu.addSeparator()
        delAction = menu.addAction(self.lang.tr("remove"))
        delAction.setIcon(QIcon(':/delete.png'))
        menu.addSeparator()
        addItemAction = menu.addAction(self.lang.tr("add_link"))
        addItemAction.setIcon(QIcon(':/add.png'))
        editgroupAction = menu.addAction(self.lang.tr("change_group"))
        editgroupAction.setIcon(QIcon(':/editgroup.png'))
        delgroupAction = menu.addAction(self.lang.tr("remove_group"))
        delgroupAction.setIcon(QIcon(':/delgroup.png'))
        openDirAction = None
        self.menuitem = self.glist[self.groupitem][self.focusitem]
        path=os.path.dirname(self.menuitem.exec.replace('"',''))
        if (len(path) > 0) and os.path.isdir(path):
            #self.openpath = path
            menu.addSeparator()
            openDirAction = menu.addAction(self.lang.tr("open_folder"))
            openDirAction.setIcon(QIcon(':/quit.png'))
        action = menu.exec_(self.sender().mapToGlobal(pos))
        if action == None: return
        if action == changeAction:
            if iconedit.iconEdit(self.menuitem,self.lang):
                if self.menuitem.__class__.__name__ == 'GTItem':
                    texcol = self.sets.get('panel.textcolor','#80000000')
                    self.menuitem.titem.setHtml(f'<div style="color: {texcol}">{self.menuitem.title}</div>')
                self.savetimer.stop()
                self.savetimer.start()
        elif action == delAction:
            gr = self.menuitem.parent
            if len(gr) < 2:
                self.doDelGroup(gr)
            else:
                gr.delitem(self.menuitem.index)
                if gr.index < len(self.glist) - 1:
                   self.glist.reposItems(gr.index+1,True)
                   if not self.anitimer.isActive(): self.anitimer.start(30)
            self.savetimer.stop()
            self.savetimer.start()

        elif action == addItemAction:
            self.doAddItem(self.menuitem.parent)
        elif action == editgroupAction:
            self.doEditGroup(self.menuitem.parent)
        elif action == delgroupAction:
            self.doDelGroup(self.menuitem.parent)

        elif action == openDirAction:
            self.startfile(path)

    def groupContextMenu(self,pos,gr):
        menu = QMenu()
        menu.setStyleSheet('background: '+self.sets.get('window.menubgcolor','#222')+'; color: '+self.sets.get('window.menucolor','#fff')+'; padding: 6px;')
        addItemAction = menu.addAction(self.lang.tr("add_link"))
        addItemAction.setIcon(QIcon(':/add.png'))
        editgroupAction = menu.addAction(self.lang.tr("change_group"))
        editgroupAction.setIcon(QIcon(':/editgroup.png'))
        delgroupAction = menu.addAction(self.lang.tr("remove_group"))
        delgroupAction.setIcon(QIcon(':/delgroup.png'))
        action = menu.exec_(self.sender().mapToGlobal(pos))
        if action == None: return
        elif action == addItemAction:
            self.doAddItem(gr)
        elif action == editgroupAction:
            self.doEditGroup(gr)
        elif action == delgroupAction:
            self.doDelGroup(gr)

    def doDelGroup(self,gr):
        self.glist.delete(gr.index)
        self.setSceneRect()
        self.savetimer.stop()
        self.savetimer.start()

    def doAddItem(self,gr):
        add,title,icon,exec = iconedit.iconAdd(self.lang)
        if not add: return
        self.appendIcon(gr.index,title,icon,exec)
        self.savetimer.stop()
        self.savetimer.start()

    def doEditGroup(self,gr):
        i = gr.index
        title,withtext = groupedit.groupEdit(gr,self.lang)
        if withtext != gr.withtext:
            grps = self.sets.sets['groups']
            grps[i]['withtext'] = withtext
            grps[i]['title'] = title
            items = grps[i]['items']
            while len(gr) > 0: gr.delitem(0,False)
            gr.withtext = withtext
            gr.setTitle(title)
            for item in items:
                gr.addItem(self.signals,item['title'],item['icon'],item['exec'],False)
            self.glist.reposItems(i)
            self.setSceneRect()
        elif title != gr.title:
            shlsr  = (len(title) > 0 and len(gr.title) == 0) or (len(gr.title) > 0 and len(title) ==0)
            gr.setTitle(title,True)
            if shlsr:
                if gr.index < len(self.glist)-1:
                    self.glist.reposItems(gr.index+1,True)
                    if not self.anitimer.isActive(): self.anitimer.start(30)
                self.setSceneRect()
        self.savetimer.stop()
        self.savetimer.start()

    def applysets(self):
        QTimer.singleShot(50, self.applystyle)
        self.ui.ltitle.setText(self.sets.get('title','Programs'))
        self.ui.ltitle.setStyleSheet('QLabel#ltitle {padding-top :6px; color: '+self.sets.get('window.titlecolor','#fff')+';}')
        self.anisteps = self.sets.get('panel.anisteps',6)
        self.anistepsclick = self.sets.get('panel.anistepsclick',4)

    def changeTitle(self,title):
        self.ui.ltitle.setText(title)
        self.sets.set('title',title)
        self.savetimer.stop()
        self.savetimer.start()

    def applystyle(self):
        style = self.sets.get('window.style', self.ui.centralwidget.styleSheet())
        self.ui.centralwidget.setStyleSheet(style)
        self.glist.loadfromsets(self.signals)
        self.setSceneRect()

    def setSceneRect(self):
        rcontent = self.gv.contentsRect();
        h = self.glist.height()
        if h < rcontent.height():
            h = rcontent.height()
        self.scene.setSceneRect(0,0,rcontent.width(), h )

    def onResize(self):
        self.setSceneRect()
        rcontent = self.gv.contentsRect();
        for l in self.glist:
            if len(l.title) > 0 and l.trect != None:
                r = l.trect.rect()
                r.setWidth(rcontent.width())
                l.trect.setRect(r)
        self.glist.reposItems()


    def savelink(self, item, path):
        fn = "".join(x for x in item.title if x.isalnum())
        fn += '.desktop'
        fn = os.path.join(path, fn)
        if os.path.exists(fn): os.remove(fn)
        with open(fn,'w') as f:
            f.write('[Desktop Entry]\n')
            f.write('Name='+item.title+'\n')
            f.write('Type=Application\n')
            f.write('NoDisplay=false\n')
            f.write('Exec='+item.exec+'\n')
            f.write('Icon='+item.icon+'\n')
            f.write('Hidden=false\n')
            f.write('Terminal=false\n')
        return fn

    def onMoved(self,item,event):
        isexec = False
        km = QApplication.keyboardModifiers()
        if km == Qt.ControlModifier and os.path.isfile(item.exec):
            fn = item.exec
            isexec = True
        else:
            fn = self.savelink(item, str(self.cdir))
        dfn = fn
        if fn[0] == '/':
            fn = 'file://'+fn
        else:
            fn = 'file:///'+fn

        mime = QtCore.QMimeData()
        mime.setUrls([QUrl(fn)])
        if item.__class__.__name__ == 'GItem':
            pix = item.pixmap().copy()
        else:
            pix = item.gitem.pixmap().copy()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)
        drag.setPixmap(pix)
        hs = pix.width() // 2
        drag.setHotSpot(QtCore.QPoint(hs,hs))
        self.mainwindow.selfdrag = True
        #if os.path.isfile(item.exec):
        if isexec:
            i = drag.exec(Qt.CopyAction | Qt.LinkAction, Qt.CopyAction)
        else:
            i = drag.exec(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)
        self.mainwindow.selfdrag = False
        #print('drag result:',i)
        if not isexec:
            if i == 2:
                gr = item.parent
                gr.delitem(item.index)
                if gr.index < len(self.glist) - 1:
                    self.glist.reposItems(gr.index+1,True)
                if not self.anitimer.isActive(): self.anitimer.start(30)
            self.tempflist.append(dfn)
            self.removetimer.start()



    def doChangeTitle(self):
        self.chtltimer.stop()
        if self.changetitle == None: return
        self.ui.ltitle.setText(self.changetitle)


    def onHover(self,item,onEnter):
        self.groupitem = -1
        self.focusitem = -1
        if onEnter:
            self.focusitem = item.index
            self.groupitem = item.parent.index
        if not item.parent.withtext:
            if onEnter:
                self.changetitle = item.title
            else:
                self.changetitle = self.sets.get('title','Programs')
            if not self.chtltimer.isActive(): self.chtltimer.start(200)
        clas = item.__class__.__name__
        if clas == 'TItem': return
        if onEnter:
            sstop = item.parent.scaled
            sstart = item.parent.defscale
        else:
            sstop = item.parent.defscale
            sstart = item.parent.scaled

        if clas == 'GTItem':
            #item.anilist['scale'].addAni(item.gitem,sstart,sstop)
            item.addAni('scale',sstart,sstop,item.gitem, maxsteps=self.anisteps)
            if onEnter:
                ostart = 0.7
                ostop = 1.0
            else:
                ostart = 1.0
                ostop = 0.7
            item.addAni('opacity',ostart,ostop,item.titem, maxsteps=self.anisteps)
        else:
            item.addAni('scale',sstart,sstop, maxsteps=self.anisteps)

        if not self.anitimer.isActive(): self.anitimer.start(30)

    def onClick(self,item):
        clas = item.__class__.__name__
        mins = 0.3
        maxs = 1.3
        steps = self.anistepsclick
        if clas == 'GTItem':
            iscale = item.gitem.scale()
            item.addAni('scale',iscale,mins,item.gitem, maxsteps = steps)
            item.addAni('scale',mins,iscale,item.gitem, maxsteps = steps)
            item.addAni('scale',iscale,maxs,item.gitem, maxsteps = steps)
            item.addAni('scale',maxs,iscale,item.gitem, maxsteps = steps)
        elif clas == 'GItem':
            iscale = item.scale()
            item.addAni('scale',iscale,mins, maxsteps = steps)
            item.addAni('scale',mins,iscale, maxsteps = steps)
            item.addAni('scale',iscale,maxs, maxsteps = steps)
            item.addAni('scale',maxs,iscale, maxsteps = steps)
        if not self.anitimer.isActive(): self.anitimer.start(30)
        proc = QtCore.QProcess()
        proc.startDetached(item.exec)


    def onRemoveTimer(self):
        self.removetimer.stop()
        while len(self.tempflist) > 0:
            fn = self.tempflist.pop(0)
            if os.path.isfile(fn):
                try:
                    os.remove(fn)
                except:
                    pass

    def onAniTimer(self):
        stop = True
        for gr in self.glist:
            if len(gr.title)>0 and gr.titem != None:
                for key in gr.titem.anilist:
                    if not gr.titem.anilist[key].doStep():
                        stop = False
                for key in gr.trect.anilist:
                    if not gr.trect.anilist[key].doStep():
                        stop = False
            for item in gr:
                for key in item.anilist:
                    if not item.anilist[key].doStep():
                        stop = False

        if stop: self.anitimer.stop()

    def insertIcon(self,groupIndex, itemIndex,title,icon,exec):
        gr = self.glist[groupIndex]

        gvr = self.gv.contentsRect()
        x,y = gr.findpos(itemIndex,gvr.width() // gr.fsize)

        item = gr.insertItem(self.signals,itemIndex,title,icon,exec)
        item.setPos(QtCore.QPointF(x,y))
        self.glist.reposItems(groupIndex,True)
        item.setScale(0)
        endscale = 1.0
        if not gr.withtext:
            endscale = gr.defscale

        item.addAni('scale',0.0, endscale, maxsteps=self.anisteps)
        r = self.scene.sceneRect()
        if r.height() < self.glist.height():
            self.setSceneRect()
        if not self.anitimer.isActive(): self.anitimer.start(30)
        self.savetimer.stop()
        self.savetimer.start()

    def appendIcon(self,groupIndex,title,icon,exec):
        gr = self.glist[groupIndex]
        gvr = self.gv.contentsRect()
        x,y = gr.findpos(len(gr),gvr.width() // gr.fsize)
        item = gr.addItem(self.signals,title,icon,exec,False)
        item.setPos(QtCore.QPointF(x,y))
        self.glist.reposItems(groupIndex,True)
        item.setScale(0)
        endscale = 1.0
        if not gr.withtext:
            endscale = gr.defscale
        item.addAni('scale',0.0, endscale, maxsteps=self.anisteps)
        r = self.scene.sceneRect()
        if r.height() < self.glist.height():
            self.setSceneRect()
        if not self.anitimer.isActive(): self.anitimer.start(30)
        self.savetimer.stop()
        self.savetimer.start()

    def dropEvent(self,view, event):
        changed = False
        if event.mimeData().hasUrls:
            isShiftMod = QApplication.keyboardModifiers() == Qt.ShiftModifier
            if self.mainwindow.selfdrag:
                if isShiftMod:
                    event.setDropAction(Qt.CopyAction)
            else:
                if not isShiftMod:
                    event.setDropAction(Qt.CopyAction)
            for url in event.mimeData().urls():
                fn = str(url.toLocalFile())
                lfn = fn.lower()
                cachepath = os.path.join(os.path.dirname(self.sets.fn),'iconcache')
                if not os.path.isdir(cachepath):
                    os.mkdir(cachepath)
                if lfn.endswith('.desktop'):
                    title,icon,exec = desktopparse.parse(self, fn, self.lang)
                elif lfn.endswith('.lnk'):
                    title,icon,exec = win.lnkparse(fn, cachepath)
                elif lfn.endswith('.exe'):
                    title = os.path.basename(fn)[:-4]
                    icon = win.saveiconfromexe(fn, 0, cachepath)
                    exec = '"'+fn+'"'
                else:
                    event.ignore()
                    return
                event.accept()
                if title != "" and icon != "" and exec != "":
                    gri = 0
                    ii = -1
                    if len(self.glist) == 0:
                        rcontent = self.gv.contentsRect();
                        self.glist.addList('', (0,0),withText = self.sets.get('panel.withtext',False))
                        gr = {'title':'','withtext': False, 'items':[]}
                    else:
                        y = event.pos().y()+self.gv.verticalScrollBar().value()
                        for i in range(len(self.glist)-1,-1,-1):
                            if y > self.glist[i].startpos[1]:
                                gri = i
                                break
                        items = self.glist[gri]
                        il = len(items)
                        if il > 0:
                            if y < items[il-1].pos().y()+items.fsize:
                                x = event.pos().x()
                                if items.withtext:
                                    ly = items[0].pos().y()+items.fsize // 2
                                    if y < ly: ii = 0
                                    else:
                                        for i in range(il-1,-1,-1):
                                            ly = items[i].pos().y()
                                            if y > ly+items.fsize // 2:
                                                ii = i+1
                                                break
                                else:
                                    ly = items[0].pos().y()+items.fsize // 2
                                    lx = items[0].pos().x()+items.fsize // 2
                                    if y < ly and x < lx:
                                        ii = 0
                                    else:
                                        for i in range(il-1,-1,-1):
                                            ly,lx = items[i].pos().y(), items[i].pos().x()
                                            if (y > ly and x > lx+items.fsize // 2):
                                                ii = i+1
                                                break


                    if ii < 0:
                        self.appendIcon(gri,title,icon,exec)
                    else:
                        self.insertIcon(gri,ii,title,icon,exec)
                    self.savetimer.stop()
                    self.savetimer.start()



def main():
    app = QApplication(sys.argv)
    panelWindow = Panel(app)
    panelWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
