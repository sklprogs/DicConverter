#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import skl_shared.shared as sh
from skl_shared.localize import _
from . import gui as gi

PATH = ''
DEBUG = False


class ProgressBar:
    
    def __init__(self):
        self.gui = gi.ProgressBar (title   = _('Conversion progress')
                                  ,icon    = gi.ICON
                                  ,height  = 120
                                  ,YScroll = False
                                  )
    
    def set_text(self,text=None):
        self.gui.set_text(text)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def update(self,count,limit):
        # Prevent ZeroDivisionError
        if limit:
            percent = round((100*count)/limit)
        else:
            percent = 0
        self.gui.update(percent)



class Extractor:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.dics = []
        self.Success = True
    
    def run(self):
        pass



class Runner:
    
    def __init__(self):
        pass
    
    def run(self):
        f = '[DicConverter] plugins.lingvo.extractor.Runner.run'
        self.timer = sh.Timer(f)
        self.timer.start()
        objs.get_progress().set_text(_('Process dictionaries'))
        objs.progress.show()
        self.iwalker = Walker()
        #sh.STOP_MES = True
        #objs.get_db().clear()
        #objs.db.save()
        self.Success = self.iwalker.Success
        if self.Success:
            self.iextract = Extractor()
            self.iextract.run()
            self.Success = self.iextract.Success
        else:
            sh.com.cancel(f)
        #objs.db.save()
        objs.progress.close()
        #sh.STOP_MES = False
        #objs.db.close()
        self.report()
    
    def report(self):
        f = '[DicConverter] plugins.lingvo.extractor.Runner.report'
        if self.Success:
            messages = []
            mes = _('Processed dictionaries (total/successful):')
            messages.append(mes)
            mes = '{}/{}'.format (len(self.iwalker.files)
                                 ,len(self.iextract.dics)
                                 )
            messages.append(mes)
            messages.append('')
            mes = _('Files:')
            messages.append(mes)
            mes = ', '.join(sorted(self.iwalker.fnames))
            messages.append(mes)
            messages.append('')
            mes = _('The operation has taken:')
            messages.append(mes)
            mes = sh.com.get_human_time(self.timer.end())
            messages.append(mes)
            mes = '\n'.join(messages)
            sh.objs.get_mes(f,mes).show_info()
        else:
            sh.com.cancel(f)



class Walker:
    
    def __init__(self):
        self.set_values()
        if PATH:
            self.reset()
    
    def reset(self):
        self.set_values()
        self.check()
        self.walk()
    
    def check(self):
        f = '[DicConverter] plugins.lingvo.extractor.Walker.check'
        if PATH:
            self.idir = sh.Directory(PATH)
            self.Success = self.idir.Success
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.idir = None
        self.files = []
        self.fnames = []
        self.Success = False
    
    def walk(self):
        f = '[DicConverter] plugins.lingvo.extractor.Walker.walk'
        if self.Success:
            for dirpath, dirnames, filenames in os.walk(self.idir.dir):
                for filename in filenames:
                    low = filename.lower()
                    if low.endswith('.lsd') or low.endswith('.lod'):
                        self.fnames.append(filename)
                        file = os.path.join(dirpath,filename)
                        self.files.append(file)
        else:
            sh.com.cancel(f)
        return self.files



class Objects:
    
    def __init__(self):
        self.db = self.progress = None
    
    def get_progress(self):
        if self.progress is None:
            self.progress = ProgressBar()
        return self.progress


objs = Objects()
