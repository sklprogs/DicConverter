#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import lingvoreader.lsdfile as lf
import skl_shared.shared as sh
from skl_shared.localize import _
from . import gui as gi

PATH = ''
DEBUG = False


class LsdFile(lf.LsdFile):
    
    def __init__(self,*args,**kwargs):
        ''' Sometimes a "utf-8 codec can't decode" message is raised
            here when calling 'lingvoreader.lsdfile.__init__'.
        '''
        f = '[DicConverter] plugins.lingvo.LsdFile.__init__'
        try:
            super().__init__(*args,**kwargs)
            self.Success = True
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes,True).show_error()
    
    def decompile(self,dirw):
        f = '[DicConverter] plugins.lingvo.extractor.LsdFile.decompile'
        if self.Success:
            if dirw:
                if sh.Directory(dirw).Success:
                    try:
                        self.parse()
                        self.dump()
                        self.write_dsl(dirw)
                        return True
                    except Exception as e:
                        mes = _('Operation has failed!\n\nDetails: {}')
                        mes = mes.format(e)
                        sh.objs.get_mes(f,mes,True).show_warning()
                else:
                    mes = _('Wrong input data: "{}"!').format(dirw)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class ProgressBar:
    
    def __init__(self):
        self.gui = gi.ProgressBar (title = _('Conversion progress')
                                  ,icon = gi.ICON
                                  ,height = 120
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
    
    def __init__(self,files):
        self.set_values()
        self.files = files
    
    def set_values(self):
        self.files = []
        self.okcount = 0
        self.Success = True
    
    def decompile(self):
        f = '[DicConverter] plugins.lingvo.extractor.Extractor.decompile'
        if self.Success:
            for i in range(len(self.files)):
                ipath = sh.Path(self.files[i])
                dirname = ipath.get_dirname()
                filename = ipath.get_filename()
                filew = os.path.join(dirname,filename+'.dsl')
                mes = _('Convert "{}" to "{}"')
                mes = mes.format(self.files[i],filew)
                sh.objs.get_mes(f,mes,True).show_info()
                objs.get_progress().update(i,len(self.files))
                if os.path.exists(filew):
                    sh.com.rep_lazy(f)
                else:
                    ''' The library requests a writable directory
                        at input, not a full path.
                    '''
                    if LsdFile(self.files[i]).decompile(dirname):
                        self.okcount += 1
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[DicConverter] plugins.lingvo.extractor.Extractor.check'
        if not self.files:
            self.Success = False
            sh.com.rep_empty(f)
    
    def run(self):
        self.check()
        self.decompile()



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
            self.iextract = Extractor(self.iwalker.files)
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
                                 ,self.iextract.okcount
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
            files = self.idir.get_subfiles()
            for file in files:
                ipath = sh.Path(file)
                if ipath.get_ext_low() == '.lsd':
                    self.files.append(file)
                    self.fnames.append(ipath.get_filename())
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
