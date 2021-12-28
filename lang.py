import locale
import json
import os


class Lang:
    def __init__(self):
        l,_ = locale.getdefaultlocale()
        l = l.lower()[0:2]
        self.lang = 'default'
        if os.path.isfile('lang.json'):
            with open('lang.json') as f:
                self.dic = json.load(f)
            values = list(self.dic.values())
            if l in values[0]:
                self.lang = l
        else:
            self.dic = {}

    def tr(self,s):
        if s in self.dic:
            return self.dic[s][self.lang]
        else:
            return s



