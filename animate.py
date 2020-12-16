#
# base class Animate, subclass ScaleAnimate when realize steps of animation
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
from PyQt5.QtCore import QPointF


class Animate:
    def __init__(self, icon, maxsteps=6):
        """инициализация анимации, где в качестве входных данных ссылка на IconInfo,
            и количество шагов анимации по умолчанию 6"""
        self.maxsteps = maxsteps
        self.curstep = 0
        self.finished = False
        self.iconinfo = icon
    def doStep(self):
        """Шаг анимации, в данной функции мы приращиваем шаг на 1,
            если шаг достиг maxsteps, то параметру finish присваивается"""
        if not self.finished: self.curstep += 1
        if self.curstep >= self.maxsteps:
            self.curstep = self.maxsteps
            self.finished = True
        
class ScaleAnimate(Animate):
    def __init__(self,icon,scalestop,maxsteps = 6):
        """Инициализируем анимацию Scale, задаём начальные и конечные параметры.
           Также смотрите документацию к функции инициализации базового класса анимации"""
        super().__init__(icon,maxsteps)
        """Для реализации стэка анимации необходимы конечные параметры scale и offset предидущей анимации"""
        self.curscale = icon.lastScale #icon.getLastScaleAnim() #icon.item.scale()
        self.currentOffset = icon.lastOffset #icon.item.pos().x()-icon.x
        self.scalestop = scalestop
        dist = scalestop - self.curscale
        self.scalestep = dist / self.maxsteps
        movedist = -dist * self.iconinfo.iconsize / 2
        self.offsetStep = movedist / self.maxsteps
        self.offsetStop = round(self.currentOffset+movedist,1)
        #Записываем конечные параметры этой анимации
        self.iconinfo.lastScale = self.scalestop
        self.iconinfo.lastOffset = self.offsetStop

    def doStep(self):
        """Шаг анимации, сдесь мы увеличиваем или уменшаем текущий scale на один шаг scalestep,
            а также отступ currentOffset, т.к. центр иконки всегда должен быть на своём месте."""
        super().doStep() #запускаем функцию родительского класса
        if self.finished: 
            self.curscale = self.scalestop
            self.currentOffset = self.offsetStop
        else:
            self.curscale += self.scalestep
            self.currentOffset += self.offsetStep
        if self.iconinfo.item == None: return    
        #дальше непосредственно происходит сама анимация
        self.iconinfo.item.setScale(self.curscale)
        self.iconinfo.item.setPos(QPointF(self.currentOffset+self.iconinfo.x,self.currentOffset+self.iconinfo.y))



