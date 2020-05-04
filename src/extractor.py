#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import get as gt


class Extractor:
    
    def __init__(self):
        self.set_values()
    
    def reset(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.simple = []
        self.phrases = []
        self.iparse = None
    
    def debug(self):
        f = '[MTExtractor] extractor.Extractor.debug'
        if self.Success:
            headers = ['SIMPLE','PHRASES','SUBJECT']
            iterable = [self.simple,self.phrases,self.iparse.xplain2]
            mes = sh.FastTable (iterable = iterable
                               ,headers  = headers
                               ,maxrow   = 50
                               ,maxrows  = 1000
                               ).run()
            sh.com.run_fast_debug(mes)
        else:
            sh.com.cancel(f)
    
    def set_phrases(self):
        f = '[MTExtractor] extractor.Extractor.set_phrases'
        if self.Success:
            if self.iparse.chunks1:
                for part1 in self.iparse.chunks1:
                    if part1:
                        chunks = part1.split(b'\x00')
                        chunks = [chunk.decode(gt.CODING,'replace') \
                                  for chunk in chunks if chunk
                                 ]
                        self.simple.append(chunks[0])
                        if len(chunks) == 1:
                            self.phrases.append(chunks[0])
                        else:
                            self.phrases.append(chunks[1])
                    else:
                        sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
                self.Success = False
        else:
            sh.com.cancel(f)
    
    def parse_typein(self,file,limit=0):
        f = '[MTExtractor] extractor.Extractor.parse_typein'
        if self.Success:
            self.iparse = gt.Parser(file)
            self.iparse.parsel_loop(limit)
            self.Success = self.iparse.Success
        else:
            sh.com.cancel(f)
    
    def translate(self,pattern):
        f = '[MTExtractor] extractor.Extractor.translate'
        if self.Success:
            iget = gt.Get(pattern)
            result = iget.run()
            if result:
                return result
            else:
                iget = gt.Get(pattern,2)
                return iget.run()
        else:
            sh.com.cancel(f)
    
    def run_lang(self,lang=1,limit=0):
        f = '[MTExtractor] extractor.Extractor.run_lang'
        if self.Success:
            if lang == 1:
                file = gt.objs.get_files().iwalker.get_typein1()
            else:
                gt.LANG1, gt.LANG2 = gt.LANG2, gt.LANG1
                gt.objs.get_files().reset()
                file = gt.objs.files.iwalker.get_typein1()
            timer = sh.Timer(f)
            timer.start()
            sh.STOP_MES = True
            self.parse_typein(file,limit)
            self.set_phrases()
            #self.debug()
            art_nos = []
            for i in range(len(self.simple)):
                art_no = self.translate(self.simple[i])
                if art_no:
                    art_no = gt.com.parse3(art_no)
                    art_no = [item[0] for item in art_no if item]
                    art_nos.append(art_no)
                else:
                    art_nos.append(_('N/A'))
            sh.STOP_MES = False
            timer.end()
            assert len(self.simple) == len(self.phrases)
            mes = _('Processed chunks (total/parsed/translated): {}/{}/{}')
            translated = 0
            for art_no in art_nos:
                if art_no != _('N/A'):
                    translated += 1
            mes = mes.format (self.iparse.origcnt
                             ,len(self.phrases)
                             ,translated
                             )
            sh.objs.get_mes(f,mes,True).show_info()
            headers = ('PHRASE','SUBJECT','ARTNO')
            iterable = [self.phrases,self.iparse.xplain2,art_nos]
            mes = sh.FastTable (iterable = iterable
                               ,headers  = headers
                               ).run()
            #TODO: elaborate path
            if lang == 1:
                filew = '/home/pete/tmp/result_en.txt'
            else:
                filew = '/home/pete/tmp/result_ru.txt'
            sh.WriteTextFile (file    = filew
                             ,Rewrite = True
                             ).write(mes)
            sh.Launch(filew).launch_default()
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.run_lang(lang=1,limit=0)
        self.reset()
        self.run_lang(lang=2,limit=0)
        


if __name__ == '__main__':
    f = '[MTExtractor] extractor.__main__'
    gt.PATH = '/home/pete/.config/mclient/dics'
    gt.DEBUG = False
    gt.objs.get_files().reset()
    Extractor().run()
