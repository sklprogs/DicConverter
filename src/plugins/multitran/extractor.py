#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
from . import get as gt
from . import gui as gi
from . import db


class ProgressBar:
    
    def __init__(self):
        self.gui = gi.ProgressBar (title   = _('Extraction progress')
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



class Commands:
    
    def __init__(self):
        pass
    
    def swap_langs(self):
        gt.LANG1, gt.LANG2 = gt.LANG2, gt.LANG1
        gt.objs.get_files().reset()
    
    def calc_ranges(self,maxlim,step,minlim=0):
        f = '[DicConverter] plugins.multitran.extractor.Commands.calc_ranges'
        ranges = []
        max_ = minlim
        while max_ <= maxlim:
            min_ = max_
            max_ += step
            if max_ > maxlim:
                max_ = maxlim
            ranges.append([min_,max_])
            max_ += 1
        sh.objs.get_mes(f,ranges,True).show_debug()
        return ranges


class Runner:
    
    def __init__(self,start_page=0,end_page=100000000):
        self.start_page = start_page
        self.end_page = end_page
    
    def run(self):
        f = '[DicConverter] plugins.multitran.extractor.Runner.run'
        self.timer = sh.Timer(f)
        self.timer.start()
        objs.get_progress().set_text(_('Prepare'))
        objs.progress.show()
        # Processing will be faster by 33% if logging is disabled
        sh.STOP_MES = True
        gt.PATH = sh.Home('DicConverter').get_conf_dir()
        gt.DEBUG = False
        objs.get_db().clear()
        objs.db.save()
        self.iextract = Extractor (start_page = self.start_page
                                  ,end_page   = self.end_page
                                  )
        self.iextract.run()
        objs.db.save()
        mes = _('Find matches ({}/{})').format(2,3)
        objs.progress.set_text(mes)
        self.icompare = Compare()
        self.icompare.run()
        objs.db.save()
        mes = _('Convert ({}/{})').format(3,3)
        objs.progress.set_text(mes)
        objs.progress.close()
        sh.STOP_MES = False
        self.Success = self.iextract.Success and self.icompare.Success
        self.report()
        objs.db.print_not_found(objs.db.table1)
        objs.db.print_not_found(objs.db.table2)
        objs.db.print_final()
        objs.db.close()
    
    def report(self):
        f = '[DicConverter] plugins.multitran.extractor.Runner.report'
        if self.Success:
            messages = []
            mes = _('Processed single records (total/parsed/translated):')
            messages.append(mes)
            mes = '{}/{}/{}'.format (self.iextract.read
                                    ,self.iextract.parsed
                                    ,self.iextract.translated
                                    )
            messages.append(mes)
            mes = _('Pairs in total/with matches/without matches:')
            messages.append(mes)
            mes = '{}/{}/{}'.format (self.icompare.matches + self.icompare.nomatches
                                    ,self.icompare.matches
                                    ,self.icompare.nomatches
                                    )
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



class Compare:
    
    def __init__(self):
        self.set_values()
        self.Success = objs.get_db().Success
    
    def set_values(self):
        self.Success = True
        self.max_ = 0
        # Number of phrases to be processed per a cycle
        self.delta = 1000
        self.data1 = None
        self.data2 = None
        self.final = []
        self.matches = 0
        self.nomatches = 0
    
    def reset_range(self):
        self.data1 = None
        self.data2 = None
        self.final = []
    
    def dump(self):
        f = '[DicConverter] plugins.multitran.extractor.Compare.dump'
        if self.Success:
            if self.final:
                for row in self.final:
                    objs.get_db().add_final(row)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def compare(self):
        f = '[DicConverter] plugins.multitran.extractor.Compare.compare'
        if self.Success:
            if self.data1 and self.data2:
                for i in range(len(self.data1)):
                    Found = False
                    for j in range(len(self.data2)):
                        if self.data1[i][0] == self.data2[j][0]:
                            ''' ARTNO,SUBJECT1,SUBJECT2,SUBJECT3
                               ,PHRASE1,PHRASE2
                            '''
                            add = [self.data1[i][0],self.data1[i][1]
                                  ,self.data1[i][2],self.data1[i][3]
                                  ,self.data1[i][4],self.data2[j][4]
                                  ]
                            self.final.append(add)
                            Found = True
                            break
                    if Found:
                        self.matches += 1
                    else:
                        self.nomatches += 1
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get_max()
        self.set_ranges()
    
    def get_max(self):
        f = '[DicConverter] plugins.multitran.extractor.Compare.get_max'
        if self.Success:
            max1 = objs.get_db().get_max_artno(objs.db.table1)
            max2 = objs.db.get_max_artno(objs.db.table2)
            if max1 and max2:
                self.max_ = min(max1,max2)
                sh.objs.get_mes(f,self.max_,True).show_debug()
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_ranges(self):
        f = '[DicConverter] plugins.multitran.extractor.Compare.set_ranges'
        if self.Success:
            ranges = com.calc_ranges(self.max_,self.delta)
            if ranges:
                for range_ in ranges:
                    objs.get_progress().update(range_[0],self.max_)
                    self.reset_range()
                    self.data1 = objs.get_db().fetch_range(objs.db.table1,range_[0],range_[1])
                    self.data2 = objs.db.fetch_range(objs.db.table2,range_[0],range_[1])
                    self.compare()
                    self.dump()
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Extractor:
    
    def __init__(self,start_page=0,end_page=100000000):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.__init__'
        self.set_values()
        self.start_page = start_page
        self.end_page = end_page
    
    def set_end_page(self):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.set_end_page'
        if self.Success:
            #NOTE: Run 'init_parsers' first
            self.end_page = min (self.end_page
                                ,len(self.iparse1.lpages)
                                ,len(self.iparse2.lpages)
                                )
        else:
            sh.com.cancel(f)
    
    def reset_cycle(self):
        self.phrases = []
        self.simple = []
        self.artnos = []
        self.iparse1.reset()
        self.iparse2.reset()
    
    def set_values(self):
        self.Success = True
        self.phrases = []
        self.simple = []
        self.artnos = []
        self.read = 0
        self.parsed = 0
        self.translated = 0
        # Number of 16K pages to process at once
        self.delta = 1
        self.lang = 1
        self.start_page = 0
        self.end_page = 100000000
    
    def set_parser(self):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.set_parser'
        if self.Success:
            if self.lang == 1:
                self.iparse = self.iparse1
            else:
                self.iparse = self.iparse2
        else:
            sh.com.cancel(f)
    
    def init_parsers(self):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.init_parsers'
        if self.Success:
            ''' #NOTE: When searching stems, we need to swap languages
                and call 'get_typein1' to get a stem file for the 2nd
                language since the search uses 'get_stems1'.
            '''
            file1 = gt.objs.get_files().iwalker.get_typein1()
            file2 = gt.objs.files.iwalker.get_typein2()
            self.iparse1 = gt.Parser(file1)
            self.iparse2 = gt.Parser(file2)
            self.iparse1.get_pages()
            self.iparse2.get_pages()
            self.Success = self.iparse1.Success and self.iparse2.Success
            self.set_parser()
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.debug'
        if self.Success:
            headers = ('PHRASE','SUBJECT','ARTNO')
            iterable = [self.phrases,self.iparse.xplain2,self.artnos]
            mes = sh.FastTable (iterable = iterable
                               ,headers  = headers
                               ,maxrow   = 50
                               ,maxrows  = 1000
                               ).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def set_phrases(self):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.set_phrases'
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
        else:
            sh.com.cancel(f)
    
    def translate(self,pattern):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.translate'
        if self.Success:
            result = gt.Get(pattern).run()
            if result:
                return result
            else:
                return gt.Get(pattern,2).run()
        else:
            sh.com.cancel(f)
    
    def dump(self):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.dump'
        if self.Success:
            for i in range(len(self.artnos)):
                for artno in self.artnos[i]:
                    subjects = self.iparse.xplain2[i]
                    if len(subjects) > 2:
                        subject1 = subjects[0]
                        subject2 = subjects[1]
                        subject3 = subjects[2]
                    elif len(subjects) > 1:
                        subject1 = subjects[0]
                        subject2 = subjects[1]
                        subject3 = -1
                    elif len(subjects) > 0:
                        subject1 = subjects[0]
                        subject2 = -1
                        subject3 = -1
                    else:
                        subject1 = -1
                        subject2 = -1
                        subject3 = -1
                    
                    data = (artno,subject1,subject2,subject3
                           ,self.simple[i],self.phrases[i]
                           ,
                           )
                    if not objs.get_db().add(data,self.lang):
                        messages = []
                        mes = 'ARTNO: "{}"'.format(artno)
                        messages.append(mes)
                        mes = 'SUBJECT1: "{}"'.format(subject1)
                        messages.append(mes)
                        mes = 'SUBJECT2: "{}"'.format(subject2)
                        messages.append(mes)
                        mes = 'SUBJECT3: "{}"'.format(subject3)
                        messages.append(mes)
                        mes = 'SIMPLE: "{}"'.format(self.simple[i])
                        messages.append(mes)
                        mes = 'PHRASE: "{}"'.format(self.phrases[i])
                        messages.append(mes)
                        mes = '\n'.join(messages)
                        sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def run_lang(self,start_page,end_page):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.run_lang'
        if self.Success:
            self.iparse.parsel_loop(start_page,end_page)
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
    
    def run_cycle(self,start_page,end_page):
        self.reset_cycle()
        self.run_lang(start_page,end_page)
        self.dump()
    
    def _run_loop(self,ranges):
        for range_ in ranges:
            objs.get_progress().update(range_[0],self.end_page)
            self.run_cycle (start_page = range_[0]
                           ,end_page   = range_[1]
                           )
    
    def run_loop(self):
        f = '[DicConverter] plugins.multitran.extractor.Extractor.run_loop'
        if self.Success:
            ranges = com.calc_ranges (minlim = self.start_page
                                     ,maxlim = self.end_page
                                     ,step   = self.delta
                                     )
            if ranges:
                mes = _('Process single records ({}) ({}/{})')
                mes = mes.format(self.iparse.bname,1,3)
                objs.get_progress().set_text(mes)
                self._run_loop(ranges)
                com.swap_langs()
                self.lang = 2
                self.set_parser()
                mes = _('Process single records ({}) ({}/{})')
                mes = mes.format(self.iparse.bname,1,3)
                objs.progress.set_text(mes)
                self._run_loop(ranges)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.init_parsers()
        self.set_end_page()
        self.run_loop()



class Objects:
    
    def __init__(self):
        self.db = self.progress = None
    
    def get_progress(self):
        if self.progress is None:
            self.progress = ProgressBar()
        return self.progress
    
    def get_db(self):
        if self.db is None:
            path = sh.Home('DicConverter').add_config('extract.db')
            self.db = db.DB(path)
        return self.db


objs = Objects()
com = Commands()


if __name__ == '__main__':
    f = '[DicConverter] plugins.multitran.extractor.__main__'
    gt.PATH = sh.Home('DicConverter').get_conf_dir()
    gt.DEBUG = False
    gt.objs.get_files().reset()
    #Extractor().run()
    objs.get_db().print('LANG1')
    objs.db.print('LANG2')
    gt.objs.files.close()
    objs.get_db().close()
