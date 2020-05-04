#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import get as gt


class Extractor:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.simple = []
        self.phrases = []
    
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
            mes = _('Processed chunks: {}/{}')
            mes = mes.format (self.iparse.origcnt
                             ,len(self.iparse.chunks1)
                             )
            sh.objs.get_mes(f,mes,True).show_info()
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
    
    def run(self):
        #'acceleration measured in g'
        file = gt.objs.get_files().iwalker.get_typein1()
        self.parse_typein(file,10)
        self.set_phrases()
        #self.debug()
        art_nos = []
        for i in range(len(self.simple)):
            art_no = self.translate(self.simple[i])
            #art_nos += gt.com.parse3(art_no)
            if art_no:
                art_no = gt.com.parse3(art_no)
                art_no = [item[0] for item in art_no if item]
                art_nos.append(art_no)
            else:
                art_nos.append(_('N/A'))
        assert len(self.simple) == len(self.phrases)
        headers = ('PHRASE','SUBJECT','ARTNO')
        iterable = [self.phrases,self.iparse.xplain2,art_nos]
        mes = sh.FastTable (iterable = iterable
                           ,headers  = headers
                           ,maxrow   = 60
                           ).run()
        sh.com.run_fast_debug(mes)
        


if __name__ == '__main__':
    f = '[MTExtractor] extractor.__main__'
    gt.PATH = '/home/pete/.config/mclient/dics'
    gt.DEBUG = False
    # Do this after changing the current language
    gt.objs.get_files().reset()
    timer = sh.Timer(f)
    timer.start()
    iextract = Extractor()
    iextract.run()
    pattern = 'acceleration measured in g'
    #pattern = 'absolute measurements'
    timer.end()
