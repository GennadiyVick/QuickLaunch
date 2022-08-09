#
# Custom setting module using json, it stores not only the
# panel settings but also all its icons.
# Copyright (C) 2020  Roganov G.V. roganovg@mail.ru
#
import os.path
import json
import os
import io
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
        with io.open(fn, encoding='utf-8') as jf:
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
        """Returns a platform-specific directory for user config settings."""
        if os.name == "nt":
            appdata = os.getenv("LOCALAPPDATA")
            if appdata:
                return Path(appdata) / "RoganovSoft" / "QuickLaunch"
            appdata = os.getenv("APPDATA")
            if appdata:
                return Path(appdata) / "RoganovSoft" / "QuickLaunch" #Path(appdata+"/RoganovSoft/QuickLaunch")
            return Path('')
        xdg_config_home = os.getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            return Path(xdg_config_home+"/RoganovSoft/QuickLaunch")
        return Path(os.path.expanduser("~")+"/.config/RoganovSoft/QuickLaunch")

