#
# base class Animate, subclass ScaleAnimate when realize steps of animation
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
# 

from PyQt5.QtCore import QPointF

class AniStack(list):
    def __init__(self,aniclass):
        super(AniStack,self).__init__()
        self.lastvalue = None
        self.aniclass = aniclass

    def addAni(self,item,startvalue,stopvalue, maxsteps = 6): #, aniclass = None
        sv = startvalue
        if len(self)>0:
            sv = self.lastvalue
        self.lastvalue = stopvalue
        if stopvalue == sv: return
        #if aniclass = None:
        #    clas = self.aniclass
        #else:
        #    clas = aniclass
        #a = clas(item,sv,stopvalue,maxsteps)
        a = self.aniclass(item,sv,stopvalue,maxsteps)
        self.append(a)

    def doStep(self):
        stop = True
        if len(self) > 0:
            a = self[0]
            a.doStep()
            if a.finished:
                self.pop(0)
            if len(self) > 0:
                stop = False
        return stop

class Animate:
    def __init__(self, item,startValue,stopValue, maxsteps=6):
        """инициализация анимации, где в качестве входных данных ссылка на Item,
            и количество шагов анимации по умолчанию 6"""
        self.maxsteps = maxsteps
        self.curstep = 0
        self.finished = False
        self.item = item
        #self.startvalue = startValue
        self.stopvalue = stopValue
        self.value = startValue
        self.step = (stopValue - startValue) / maxsteps

    def doStep(self):
        """Шаг анимации, в данной функции мы приращиваем шаг на 1,
            если шаг достиг maxsteps, то параметру finished присваивается True"""
        if not self.finished: self.curstep += 1
        if self.curstep >= self.maxsteps:
            self.curstep = self.maxsteps
            self.finished = True
        if self.finished:
            self.value = self.stopvalue
        else:
            self.value += self.step



class OpacityAnimate(Animate):
    def doStep(self):
        super().doStep()
        self.item.setOpacity(self.value)

class ScaleAnimate(Animate):
    def doStep(self):
        super().doStep()
        self.item.setScale(self.value)

class MoveAnimate(Animate):
    def doStep(self):
        super().doStep()
        self.item.setPos(self.value)


class ScrollAnimate:
    def __init__(self, sb):
        self.sb = sb
        self.pos = sb.value()
        self.lpos = self.pos
        self.step = 6
        self.finished = True

    def doStep(self):
        self.pos += self.step
        if self.step > 0:
            if self.pos >= self.lpos:
                self.finished = True
        else:
            if self.pos <= self.lpos:
                self.finished = True
        if self.finished:
            self.pos = self.lpos
        self.sb.setValue(self.pos)



