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
        super().__init__(*args,**kwargs)
    
    def run(self):
        f = '[DicConverter] plugins.lingvo.extractor.LsdFile.run'
        try:
            self.parse()
            self.dump()
            return self.extract()
        except Exception as e:
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes,True).show_warning()
        
    def extract(self):
        iwrite = io.StringIO()
        iwrite.write('#NAME\t\"')
        iwrite.write(self.name)
        iwrite.write('\"\n')
        iwrite.write('#INDEX_LANGUAGE\t\"')
        iwrite.write(lf.tools.lang_map[self.header.source_language])
        iwrite.write('\"\n')
        iwrite.write('#CONTENTS_LANGUAGE\t\"')
        iwrite.write(lf.tools.lang_map[self.header.target_language])
        iwrite.write('\"\n')
        if self.icon_size > 0:
            base, orig_ext = os.path.splitext(os.path.basename(self.filename))
            iwrite.write('#ICON_FILE\t\"')
            iwrite.write(base)
            iwrite.write('.bmp\"\n"')
        iwrite.write('\n')
        for h, r in self.dict:
            if h.simple:
                iwrite.write(h.get_first_ext_text())
                iwrite.write('\n\t')
            else:
                for item in h.headings:
                    iwrite.write(item.ext_text)
                    iwrite.write('\n')
                iwrite.write('\t')
            iwrite.write(self.normalize_article(r))
            iwrite.write('\n')
        text = iwrite.getvalue()
        iwrite.close()
        return text



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
    
    def __init__(self,files):
        self.set_values()
        self.files = files
    
    def set_values(self):
        self.dics = []
        self.files = []
        self.Success = True
    
    def decompile(self):
        f = '[DicConverter] plugins.lingvo.extractor.Extractor.decompile'
        if self.Success:
            #cur #TODO: del
            self.files = self.files[:1]
            for i in range(len(self.files)):
                ipath = sh.Path(self.files[i])
                dirname = ipath.get_dirname()
                basename = ipath.get_basename()
                filew = os.path.join(dirname,basename+'.dsl')
                mes = _('Convert "{}" to "{}"')
                mes = mes.format(self.files[i],filew)
                sh.objs.get_mes(f,mes,True).show_info()
                objs.get_progress().update(i,len(self.files))
                self.dics.append(LsdFile(self.files[i]).run())
            self.dics = [dic for dic in self.dics if dic]
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[DicConverter] plugins.lingvo.extractor.Extractor.check'
        if not self.files:
            self.Success = False
            sh.com.rep_empty(f)
    
    def debug(self):
        f = '[DicConverter] plugins.lingvo.extractor.Extractor.debug'
        if self.Success:
            sh.com.run_fast_debug(f,'\n\n'.join(self.dics))
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.decompile()
        self.debug()



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
