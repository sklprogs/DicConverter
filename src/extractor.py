#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import get as gt


class Extractor:
    
    def __init__(self):
        f = '[MTExtractor] extractor.Extractor.__init__'
        self.set_values()
        ihome = sh.Home('DicExtractor')
        self.filew1 = ihome.add_config('result1.txt')
        self.filew2 = ihome.add_config('result2.txt')
        # Rewrite files if they exist (since we further use appending)
        sh.WriteTextFile(self.filew1,True).write('\n')
        sh.WriteTextFile(self.filew2,True).write('\n')
        self.timer = sh.Timer(f)
        self.timer.start()
    
    def reset_cycle(self):
        self.phrases = []
        self.simple = []
        self.artnos = []
        self.iparse = None
    
    def set_values(self):
        self.Success = True
        self.phrases = []
        self.simple = []
        self.artnos = []
        self.iparse = None
        self.read = 0
        self.parsed = 0
        self.translated = 0
    
    def report(self):
        f = '[MTExtractor] extractor.Extractor.report'
        if self.Success:
            messages = []
            mes = _('Processed chunks (total/parsed/translated):')
            messages.append(mes)
            mes = '{}/{}/{}'
            mes = mes.format(self.read,self.parsed,self.translated)
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
    
    def debug(self):
        f = '[MTExtractor] extractor.Extractor.debug'
        if self.Success:
            headers = ('PHRASE','SUBJECT','ARTNO')
            iterable = [self.phrases,self.iparse.xplain2,self.artnos]
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
    
    def parse_typein(self,file,start_page=0,end_page=100000000):
        f = '[MTExtractor] extractor.Extractor.parse_typein'
        if self.Success:
            self.iparse = gt.Parser(file)
            self.iparse.parsel_loop(start_page,end_page)
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
    
    def dump(self):
        f = '[MTExtractor] extractor.Extractor.dump'
        if self.Success:
            iterable = [self.phrases,self.iparse.xplain2,self.artnos]
            mes = sh.FastTable(iterable).run()
            sh.WriteTextFile (file    = self.filew
                             ,Rewrite = True
                             ).append(mes)
        else:
            sh.com.cancel(f)
    
    def run_lang(self,lang=1,start_page=0,end_page=100000000):
        f = '[MTExtractor] extractor.Extractor.run_lang'
        if self.Success:
            if lang == 1:
                file = gt.objs.get_files().iwalker.get_typein1()
                self.filew = self.filew1
            else:
                gt.LANG1, gt.LANG2 = gt.LANG2, gt.LANG1
                gt.objs.get_files().reset()
                file = gt.objs.files.iwalker.get_typein1()
                self.filew = self.filew2
            self.parse_typein(file,start_page,end_page)
            self.set_phrases()
            #self.debug()
            for i in range(len(self.simple)):
                artno = self.translate(self.simple[i])
                if artno:
                    artno = gt.com.parse3(artno)
                    artno = [item[0] for item in artno if item]
                    self.artnos.append(artno)
                else:
                    self.artnos.append([-1])
            
            self.read += self.iparse.origcnt
            self.parsed += len(self.phrases)
            
            assert len(self.simple) == len(self.phrases)
            for artno in self.artnos:
                if artno != [-1]:
                    self.translated += 1
        else:
            sh.com.cancel(f)
    
    def run_cycle(self,lang=1,start_page=0,end_page=100000000):
        self.run_lang (lang       = lang
                      ,start_page = start_page
                      ,end_page   = end_page
                      )
        self.dump()
        self.reset_cycle()
    
    def run(self):
        start_page = 0
        end_page = 100000000
        sh.STOP_MES = True
        
        self.run_cycle (lang       = 1
                       ,start_page = start_page
                       ,end_page   = end_page
                       )
        self.run_cycle (lang       = 2
                       ,start_page = start_page
                       ,end_page   = end_page
                       )

        sh.STOP_MES = False
        self.report()

        sh.Launch(self.filew1).launch_default()
        sh.Launch(self.filew2).launch_default()


if __name__ == '__main__':
    f = '[MTExtractor] extractor.__main__'
    gt.PATH = sh.Home('DicExtractor').get_conf_dir()
    gt.DEBUG = False
    gt.objs.get_files().reset()
    Extractor().run()
