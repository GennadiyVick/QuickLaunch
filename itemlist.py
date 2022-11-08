#
# GroupList, ItemList classes
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
#
from myitem import TItem,GItem,GTItem, RItem
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QBrush

class GroupList(list):
    def __init__(self, scene, sets, gv):
        super(GroupList,self).__init__()
        self.sets = sets
        self.scene = scene
        self.gv = gv


    def addList(self, title = '', startPos = (0,0), withText = None, shlrepos = True):
        withtext = withText
        if withtext == None:
            withtext = self.sets.get('panel.withtext',False) #self.sets.withtext
        l = ItemList(self, title, withtext, startPos )
        l.index = len(self)
        self.append(l)
        if shlrepos: self.reposItems()
        return l

    def reposItems(self, startIndex = 0, animate = False):
        #print('reposItems, startIndex = ',startIndex,'animate = ',animate)
        if startIndex == 0:
            pos = 0
        else:
            pos = self[startIndex-1].startpos[1]+self[startIndex-1].height
        for i in range(startIndex,len(self)):
            l = self[i]
            l.setStartPos((0,pos),animate)
            #print(f'[{l.title}]', f'l({i}).startpos = ',l.startpos)
            pos += l.height

    def height(self):
        h = 0
        for l in self:
            h += l.height
        return h

    def delete(self,index, repos = True):
        l = self[index]
        if l.titem != None:
            self.scene.removeItem(l.titem)
        if l.trect != None:
            self.scene.removeItem(l.trect)
        while len(l) > 0:
            l.delitem(0, repos = False)
        self.pop(index)
        #del self[index]
        if (index < len(self)) and repos:
            self.reposItems(index)
        self.reindex()

    def reindex(self):
        l = len(self)
        if l == 0: return
        for i in range(l):
            self[i].index = i

    def setItemTitle(self,index,title, repos = True):
        shlRepos = (len(self[index].title) == 0 and len(title) > 0) or (len(self[index].title) > 0 and len(title) == 0)
        self[index].setTitle(title)
        if shlRepos and repos:
            self.reposItems(index,True)

    def savetosets(self):
        gl = []
        for g in self:
            gr = {'title': g.title, 'withtext': g.withtext}
            items = []
            for item in g:
                itm = {'title': item.title,'icon': item.icon,'exec': item.exec}
                items.append(itm)
            gr['items'] = items
            gl.append(gr)
        self.sets.sets['groups'] = gl

    def loadfromsets(self,signals,repos = True):
        #print('begin load')
        while len(self) > 0: self.delete(0, False)
        rcontent = self.gv.contentsRect();
        if not ('groups' in self.sets.sets): return
        for gr in self.sets.sets['groups']:
            #print('add list',f"[{gr['title']}]",len(gr['items']))
            if len(gr['items']) > 0:
                gl = self.addList(gr['title'], (0,0), withText = gr['withtext'], shlrepos = False)
                for item in gr['items']:
                    item = gl.addItem(signals,item['title'],item['icon'],item['exec'], False)
        if repos: self.reposItems()
        self.reindex()


class ItemList(list):
    def __init__(self, parent, title = '', withText = False, startPos = (0,0)):
        super(ItemList,self).__init__()
        self.parent = parent
        self.sets = parent.sets
        self.gv = parent.gv
        self.scene = parent.scene
        self.titem = None
        self.trect = None
        self.title = ''
        self.titletext = title
        self.index = -1
        self.startpos = startPos
        self.deficonsize = self.sets.get('panel.defaulticonsize', 48)
        iconsize = self.sets.get('panel.iconsize',32)
        scalsesize = self.sets.get('panel.scalediconsize', 48)
        self.defscale = iconsize / self.deficonsize
        self.scaled = scalsesize / self.deficonsize
        if iconsize < self.deficonsize:
            self.hinterval = round(abs(self.deficonsize - iconsize) / 2)
        else:
            self.hinterval = 0
        #self.hinterval += self.sets.get('panel.iconinterval',0)
        self.fsize = iconsize+self.hinterval+self.sets.get('panel.iconinterval',0)


        self.titleoffset = 0
        self.height = 0


        self.withtext = withText

        if len(title) > 0:
            self.setTitle(title)

    def setTitle(self, title, reposItems = False):
        if len(self.title) == 0:
            if len(title) == 0: return
            self.titem = TItem(self)
            self.titem.index = -1
            self.titem.setPos(self.startpos[0],self.startpos[1])
            #self.titem.document().setPageSize(QSizeF(50,50));
            self.titem.setVisible(True)
            self.scene.addItem(self.titem)

            rect = self.titem.boundingRect()
            r = self.gv.contentsRect()
            rect.setWidth(r.width())
            if rect.height() < 24:
                rect.setHeight(24)

            self.titleoffset = rect.height()
            self.trect = RItem(self)
            self.trect.setRect(rect)
            self.trect.setPen(QColor(self.sets.get('group.titlebordercolor','#238')))
            self.trect.setBrush(QBrush(QColor(self.sets.get('group.titlebgcolor','#222'))))
            self.trect.setPos(self.startpos[0],self.startpos[1])
            self.trect.setVisible(True)
            self.scene.addItem(self.trect)
            self.trect.setZValue(-1);
        elif len(title) == 0:
            if self.titem != None:
                self.scene.removeItem(self.titem)
                del self.titem

            if self.trect != None:
                self.scene.removeItem(self.trect)
                del self.trect
            self.titleoffset = 0
        self.title = title
        if len(title) > 0:
            grcol = self.sets.get('group.titlecolor','#fff')
            if self.titem != None:
                self.titem.setHtml(f'<div style="color: {grcol}">{title}</div>')
        if reposItems:
            self.repositems()


    def setStartPos(self, pos, animate = False):
        self.startpos = pos
        #print('set startpos ',self.title, pos, 'titem=None is', self.titem == None)
        if len(self.title) > 0 and self.titem != None:
            if animate:
                self.titem.addAni('move',self.titem.pos(),QPointF(self.startpos[0],self.startpos[1]))
                self.trect.addAni('move',self.trect.pos(),QPointF(self.startpos[0],self.startpos[1]))
            else:
                self.titem.setPos(self.startpos[0],self.startpos[1])
                self.trect.setPos(self.startpos[0],self.startpos[1])
        self.repositems(0, animate)

    def delitem(self, index, repos = True, updatescene = False):
        self.scene.removeItem(self.pop(index))
        self.scene.update
        #self.pop(index)
        for i in range(len(self)):
            self[i].index = i
        if repos:
            self.repositems(index, animate = True)
        elif updatescene:
            self.scene.update

    def findpos(self,i,c):
        if self.withtext:
            x = self.startpos[0]
            y = i * self.fsize + self.startpos[1] + self.titleoffset
        else:
            x = int((i % c) * self.fsize) + self.startpos[0]
            y = int((i // c) * self.fsize) + self.startpos[1] + self.titleoffset
        return x,y

    def repositems(self, startIndex = 0, animate = False):
        cnt = len(self)

        if cnt == 0:
            self.height = self.titleoffset
            return
        elif startIndex >= cnt:
            r = self.gv.contentsRect()
            c = r.width() // self.fsize
            if self.withtext:
                self.height = self.titleoffset+(cnt * self.fsize) + self.hinterval
            else:
                self.height = self.titleoffset+ (((cnt-1) // c + 1) * self.fsize) + self.hinterval
            return

        r = self.gv.contentsRect()
        c = r.width() // self.fsize
        if c == 0: c = 1

        for i in range(startIndex,cnt):
            item = self[i]
            x,y = self.findpos(i,c)
            if animate:
                item.addAni('move',item.pos(),QPointF(x,y))
            else:
                item.setPos(x, y)

        if self.withtext:
            self.height = self.titleoffset+(cnt * self.fsize) + self.hinterval
        else:
            self.height = self.titleoffset+ (((cnt-1) // c + 1) * self.fsize) + self.hinterval


    def addItem(self,signals,title,icon,exec, repos = True):
        i = len(self)
        if self.withtext:
            item = GTItem(self,signals, icon,title, exec)
        else:
            item = GItem(self, signals, icon,title, exec)
        item.index = i
        item.setVisible(True)
        if item.__class__.__name__ == 'GTItem':
            item.gitem.setScale(self.defscale)
        else:
            item.setScale(self.defscale)
        self.append(item)
        self.scene.addItem(item)
        if repos: self.repositems(i,True)
        return item


    def insertItem(self,signals,itemIndex,title,icon,exec):
        if self.withtext:
            item = GTItem(self,signals, icon,title, exec)
        else:
            item = GItem(self,signals, icon,title, exec)
        item.setVisible(True)
        if item.__class__.__name__ == 'GTItem':
            item.gitem.setScale(self.defscale)
        else:
            item.setScale(self.defscale)
        item.scaled = self.scaled
        item.defscale = self.defscale
        self.insert(itemIndex,item)
        self.scene.addItem(item)
        for i in range(len(self)):
            self[i].index = i
        return item


    def setVisible(self, index, visible = True):
        item = self[index]
        item.visible = visible
        item.setVisible(visible)
        self.repositems()

    def visibleCount(self):
        cnt = 0
        for item in self:
            if item.visible:
                cnt += 1
        return cnt
