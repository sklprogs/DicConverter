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
        self.subjects = []
    
    def debug(self):
        f = '[MTExtractor] extractor.Extractor.debug'
        if self.Success:
            headers = ['SIMPLE','PHRASES','SUBJECT']
            iterable = [self.simple,self.phrases,self.subjects]
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
    
    def parse_typein(self):
        f = '[MTExtractor] extractor.Extractor.parse_typein'
        if self.Success:
            self.iparse = gt.Parser(gt.objs.get_files().iwalker.get_typein1())
            self.iparse.parsel_loop(10)
            self.subjects = list(self.iparse.xplain2)
            mes = _('Number of chunks: {}').format(len(self.iparse.chunks1))
            sh.objs.get_mes(f,mes,True).show_debug()
            self.Success = self.iparse.Success
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.parse_typein()
        self.set_phrases()


if __name__ == '__main__':
    f = '[MTExtractor] extractor.__main__'
    gt.PATH = '/home/pete/.config/mclient/dics'
    gt.DEBUG = False
    timer = sh.Timer(f)
    timer.start()
    iextract = Extractor()
    iextract.run()
    timer.end()
    iextract.debug()
