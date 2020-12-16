#
# class IconList based list class with save and load method
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
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QTextStream
from PyQt5.QtCore import QSize
from iconinfo import IconInfo


class IconList(list):
    def __init__(self,parent):
        self.parent = parent
        self.defaultIconScaledSize = parent.defaultIconScaledSize
        self.defaultIconFrameSize = parent.defaultIconFrameSize
        self.defaultIconSize = parent.defaultIconSize
        
    def loadFromFile(self,fn,scene):
        if (not QFile.exists(fn)): return
        file = QFile(fn)
        colcnt = scene.width() / self.defaultIconFrameSize
        if (file.open(QFile.ReadOnly | QFile.Text)):
            stream = QTextStream(file)
            while (not stream.atEnd()):
                line = stream.readLine()
                lst = line.split(";")
                l = len(lst)
                title = ""
                icon = ""
                exec = ""
                if l > 0: title = lst[0]
                if l > 1: icon = lst[1]
                if l > 2: exec = lst[2]                        
                if icon != "" and exec != "":
                    if not self.addItem(icon,exec,title):
                        print("item not added ("+title+")")

        file.close()

    def saveToFile(self,fn):
        file = QFile(fn)
        if file.exists(): file.remove()
        if file.open(QFile.WriteOnly):
            stream = QTextStream(file)
            for inf in self:
                line = inf.getLine()+"\n"
                stream << line
            file.close()

    def cnt(self):
        return len(self)

    def addItem(self,icon,exec,title):
        #в iconinfo  наоборот iconsize = 48 scaled size = 32, а тут наоборот defaultIconScaledSize = 48
        info = IconInfo(self.defaultIconScaledSize,self.defaultIconSize,self.defaultIconFrameSize)
        info.title = title
        info.exec = exec
        info.icon = icon
        

        cnt = self.cnt()
        x = int((cnt % self.parent.colcnt) * self.defaultIconFrameSize)+8
        y = int((cnt // self.parent.colcnt) * self.defaultIconFrameSize)+8
        if not info.createIconItem(self.parent.scn,x,y): return False
   
        self.append(info)
        rowcnt = int(self.parent.height() // self.defaultIconFrameSize)
        if self.cnt() == 0: return
        row = int((self.cnt()-1) // self.parent.colcnt)

        if row >= rowcnt:
            h = row * self.defaultIconFrameSize + self.defaultIconFrameSize+36
            self.parent.prnt.setFixedSize(QSize(self.parent.prnt.ui.width,h))
            self.parent.prnt.scn.setSceneRect(0,0, self.parent.prnt.width()-3, self.parent.prnt.height()-26)
        self.saveToFile(self.parent.listfn)
        return True

        
