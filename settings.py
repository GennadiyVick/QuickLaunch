import os.path
import json
import os
from pathlib import Path

class Settings():
    def __init__(self,fn, onApply = None):
        self.sets = {}
        self.fn = fn
        self.onApply = onApply
        if not self.load(fn):
            self.sets['title'] = 'UnTitled'
        #self.applysets()

    def save(self):
        with open(self.fn, 'w', encoding='utf-8') as f:
            json.dump(self.sets, f, ensure_ascii=False, indent=4)

    def load(self,fn):
        if not os.path.isfile(fn): return False
        jf =  open(fn)
        self.sets = json.load(jf)
        return self.sets != None

    def getbykey(self,item,key, create = False, listcreate = False):
        result = None
        cls = item.__class__.__name__
        if cls == 'list':
            if not key.isdigit(): return None
            index = int(key)
            if index >= len(item): return None
            result = item[index]
        elif cls == 'dict':
            if not (key in item):
                if create:
                    if listcreate:
                        item[key] = []
                    else:
                        item[key] = {}
                else:
                    return None
            result = item[key]
        else:
            result = item
        return result

    def get(self,keystring, default = None, parent = None):
        keys = keystring.split('.')
        if parent == None:
            item = self.sets
        else:
            item = parent
        for key in keys:
            item = self.getbykey(item,key)
            if item == None: return default
        return item


    def set(self,keystring, value, parent = None):
        keys = keystring.split('.')
        if parent == None:
            item = self.sets
        else:
            item = parent
        keyslen = len(keys)
        for i in range(keyslen-1):
            item = self.getbykey(item,keys[i],True, (i<keyslen-1) and (keys[i+1] == '-1' or keys[i+1].isdigit()))
            if item == None: return False
        key = keys[len(keys)-1]
        if item.__class__.__name__ == 'list':
            if key == '-1':
                item.append(value)
            else:
                if not key.isdigit(): return False
                index = int(key)
                if index >= len(item):
                    item.append(value)
                else:
                    item[index] = value
        else:
            item[key] = value
        return True

    def getConfigDir():
        """Returns a platform-specific root directory for user config settings."""
        if os.name == "nt":
            appdata = os.getenv("LOCALAPPDATA")
            if appdata:
                return Path(appdata+"/RoganovSoft/QuickLaunch")
            appdata = os.getenv("APPDATA")
            if appdata:
                return Path(appdata+"/RoganovSoft/QuickLaunch")
            return Path('')
        xdg_config_home = os.getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            return Path(xdg_config_home+"/RoganovSoft/QuickLaunch")
        return Path(os.path.expanduser("~")+"/.config/RoganovSoft/QuickLaunch")
'''
    def applysets(self):
        if self.sets == None: return
        self.deficonsize =  self.sets.get('panel.defaulticonsize', 48)
        iconsize = self.sets.get('panel.iconsize',32)
        scalsesize = self.sets.get('panel.scalediconsize', 48)
        self.defscale = iconsize / self.deficonsize
        self.scaled = scalsesize / self.deficonsize
        self.withtext = self.sets.get('panel.withtext',False)
        self.shaddowoffset = self.sets.get('panel.shaddowoffsetx',2.0)
        self.shaddowoffsetg = self.sets.get('panel.shaddowgause',6.0)
        self.shaddowcolor = self.sets.get('panel.shaddowcolor','#80000000')
        self.textcolor = self.sets.get('panel.textcolor','#80000000')
        self.shaddow = self.sets.get('panel.shaddow',False)
        self.groupcolor = self.sets.get('group.titlecolor','#fff')
        self.groupbgcolor = self.sets.get('group.titlebgcolor','#40000000')
        self.groupbordercolor = self.sets.get('group.titlebordercolor','#2000ffff')
        if self.onApply != None:
            self.onApply.emit()
'''
