#
# base class Animate, subclass ScaleAnimate when realize steps of animation
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
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
        self.curscale = icon.lastScale #icon.getLastScaleAnim() #icon.item.scale()
        self.currentOffset = icon.lastOffset #icon.item.pos().x()-icon.x
        self.scalestop = scalestop
        dist = scalestop - self.curscale
        self.scalestep = dist / self.maxsteps
        movedist = -dist * self.iconinfo.iconsize / 2
        self.offsetStep = movedist / self.maxsteps
        self.offsetStop = round(self.currentOffset+movedist,1)
        self.iconinfo.lastScale = self.scalestop
        self.iconinfo.lastOffset = self.offsetStop

    def doStep(self):
        """Шаг анимации, сдесь мы увеличиваем или уменшаем текущий scale на один шаг scalestep,
            а также отступ currentOffset, т.к. центр иконки всегда должен быть на своём месте."""
        super().doStep()
        if self.finished: 
            self.curscale = self.scalestop
            self.currentOffset = self.offsetStop
        else:
            self.curscale += self.scalestep
            self.currentOffset += self.offsetStep
        if self.iconinfo.item == None: return    
        self.iconinfo.item.setScale(self.curscale)
        self.iconinfo.item.setPos(QPointF(self.currentOffset+self.iconinfo.x,self.currentOffset+self.iconinfo.y))



