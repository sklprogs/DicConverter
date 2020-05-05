#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import skl_shared.shared as sh
from skl_shared.localize import _
import get as gt


class DB:

    def __init__(self,path):
        self.set_values()
        self.path = path
        self.connect()
        self.create_tab1()
        self.create_tab2()
    
    def set_values(self):
        self.Success = True
        self.path = ''
        self.db = self.dbc = None
    
    def print (self,table='LANG1'
              ,maxrow=50,maxrows=1000
              ):
        f = '[MTExtractor] extractor.DB.print'
        if self.Success:
            subquery = 'select {} from {} order by ARTNO desc limit ?'
            
            query = subquery.format('ARTNO',table)
            self.dbc.execute(query,(maxrows,))
            artnos = self.dbc.fetchall()
            if artnos:
                artnos = [artno[0] for artno in artnos]
            else:
                artnos = []
            
            query = subquery.format('SUBJECT1',table)
            self.dbc.execute(query,(maxrows,))
            subjects = self.dbc.fetchall()
            if subjects:
                subjects = [subject[0] for subject in subjects]
            else:
                subjects = []
            
            query = subquery.format('PHRASE',table)
            self.dbc.execute(query,(maxrows,))
            phrases = self.dbc.fetchall()
            if phrases:
                phrases = [phrase[0] for phrase in phrases]
            else:
                phrases = []
            
            headers = ('NO','ARTNO','SUBJECT','PHRASE')
            nos = [i + 1 for i in range(len(subjects))]
            iterable = [nos,artnos,subjects,phrases]
            mes = sh.FastTable (iterable = iterable
                               ,headers  = headers
                               ,maxrow   = maxrow
                               ,maxrows  = maxrows
                               ).run()
            sh.com.run_fast_debug(mes)
        else:
            sh.com.cancel(f)
    
    def add1(self,data):
        f = '[MTExtractor] extractor.DB.add1'
        if self.Success:
            try:
                self.dbc.execute ('insert into LANG1 values (?,?,?,?,?)'
                                 ,data
                                 )
                return True
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def add2(self,data):
        f = '[MTExtractor] extractor.DB.add2'
        if self.Success:
            try:
                self.dbc.execute ('insert into LANG2 values (?,?,?,?,?)'
                                 ,data
                                 )
                return True
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = '[MTExtractor] extractor.DB.save'
        if self.Success:
            if self.path:
                mes = _('Save "{}"').format(self.path)
                sh.objs.get_mes(f,mes,True).show_info()
                try:
                    self.db.commit()
                except Exception as e:
                    self.fail(f,e)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def clear(self):
        f = '[MTExtractor] extractor.DB.clear'
        mes = _('Delete all records from {}').format('LANG1, LANG2')
        sh.objs.get_mes(f,mes,True).show_warning()
        self.dbc.execute('delete from LANG1')
        self.dbc.execute('delete from LANG2')
        #TODO: vacuumize
    
    def create_tab1(self):
        f = '[MTExtractor] extractor.DB.create_tab1'
        if self.Success:
            try:
                self.dbc.execute (
                    'create table if not exists LANG1 (\
                     ARTNO    integer \
                    ,SUBJECT1 integer \
                    ,SUBJECT2 integer \
                    ,SUBJECT3 integer \
                    ,PHRASE   text \
                                                      )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_tab2(self):
        f = '[MTExtractor] extractor.DB.create_tab2'
        if self.Success:
            try:
                self.dbc.execute (
                    'create table if not exists LANG2 (\
                     ARTNO    integer \
                    ,SUBJECT1 integer \
                    ,SUBJECT2 integer \
                    ,SUBJECT3 integer \
                    ,PHRASE   text \
                                                      )'
                                 )
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[MTExtractor] extractor.DB.close'
        if self.Success:
            mes = _('Close "{}"').format(self.path)
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                self.dbc.close()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def fail(self,func,error):
        self.Success = False
        mes = _('Database "{}" has failed!\n\nDetails: {}')
        mes = mes.format(self.path,error)
        sh.objs.get_mes(func,mes).show_warning()
    
    def connect(self):
        f = '[MTExtractor] extractor.DB.connect'
        if self.Success:
            mes = _('Open "{}"').format(self.path)
            sh.objs.get_mes(f,mes,True).show_info()
            try:
                self.db = sqlite3.connect(self.path)
                self.dbc = self.db.cursor()
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)



class Extractor:
    
    def __init__(self):
        f = '[MTExtractor] extractor.Extractor.__init__'
        self.set_values()
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
    
    def dump(self,lang):
        f = '[MTExtractor] extractor.Extractor.dump'
        if self.Success:
            if lang == 1:
                action = objs.get_db().add1
            else:
                action = objs.get_db().add2
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
                           ,self.phrases[i]
                           ,
                           )
                    if not action(data):
                        messages = []
                        mes = 'ARTNO: "{}"'.format(artno)
                        messages.append(mes)
                        mes = 'SUBJECT1: "{}"'.format(subject1)
                        messages.append(mes)
                        mes = 'SUBJECT2: "{}"'.format(subject2)
                        messages.append(mes)
                        mes = 'SUBJECT3: "{}"'.format(subject3)
                        messages.append(mes)
                        mes = 'PHRASE: "{}"'.format(self.phrases[i])
                        messages.append(mes)
                        mes = '\n'.join(messages)
                        sh.objs.get_mes(f,mes).show_error()
                                           
            objs.db.save()
        else:
            sh.com.cancel(f)
    
    def run_lang(self,lang=1,start_page=0,end_page=100000000):
        f = '[MTExtractor] extractor.Extractor.run_lang'
        if self.Success:
            if lang == 1:
                file = gt.objs.get_files().iwalker.get_typein1()
            else:
                gt.LANG1, gt.LANG2 = gt.LANG2, gt.LANG1
                gt.objs.get_files().reset()
                file = gt.objs.files.iwalker.get_typein1()
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
        self.dump(lang)
        self.reset_cycle()
    
    def run(self,end_page=100000000):
        start_page = 0
        sh.STOP_MES = True
        objs.get_db().clear()
        objs.db.save()
        
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
        objs.get_db().print('LANG1')
        objs.db.print('LANG2')



class Objects:
    
    def __init__(self):
        self.db = None
    
    def get_db(self):
        if self.db is None:
            path = sh.Home('DicExtractor').add_config('extract.db')
            self.db = DB(path)
        return self.db


objs = Objects()


if __name__ == '__main__':
    f = '[MTExtractor] extractor.__main__'
    gt.PATH = sh.Home('DicExtractor').get_conf_dir()
    gt.DEBUG = False
    gt.objs.get_files().reset()
    #Extractor().run()
    objs.get_db().print('LANG1')
    objs.db.print('LANG2')
    gt.objs.files.close()
    objs.get_db().close()
