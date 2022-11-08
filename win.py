from icoextract import get_icon
from lnkfile import getLinkInfo
import os

def saveiconfromexe(exe, index, cachepath):
    fn = os.path.basename(exe)+'.ico'
    savefn = os.path.join(cachepath, fn)
    if os.path.isfile(savefn):
        return savefn
    if get_icon(exe,savefn,int(index)):
        return savefn
    else:
        return ':/icon.png'

def lnkparse(fn, cachepath):
    info = getLinkInfo(fn)
    title = os.path.basename(fn)[:-4]
    exec = '"'+info['runfile']+'"'
    if 'commandLineArguments' in info:
        exec += ' ' + info['commandLineArguments']
    if 'iconLocation' in info:
        icon = info['iconLocation']
    else:
        icon = info['runfile']
    imageindex = 0
    if ',' in icon:
        iconindex = int(icon[icon.index(',')+1:])
        icon = icon[:icon.index(',')]
    if icon[-4:].lower() in '.exe.dll':
        icon = saveiconfromexe(icon,imageindex, cachepath)
    return title, icon, exec


