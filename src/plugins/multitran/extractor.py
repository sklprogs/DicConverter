#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import skl_shared.shared as sh
from skl_shared.localize import _
from . import get as gt


class Commands:
    
    def __init__(self):
        pass
    
    def calc_ranges(self,limit,delta):
        f = '[DicExtractor] plugins.multitran.extractor.Commands.calc_ranges'
        ranges = []
        max_ = 1
        while max_ <= limit:
            min_ = max_
            max_ += delta
            if max_ > limit:
                max_ = limit
            ranges.append([min_,max_])
            max_ += 1
        sh.objs.get_mes(f,ranges,True).show_debug()
        return ranges



class Compare:
    
    def __init__(self):
        self.set_values()
        self.Success = objs.get_db().Success
    
    def set_values(self):
        self.Success = True
        self.max_ = 0
        ''' Number of phrases to be processed per a cycle. Each cycle
            is followed by committing to DB, so this number should be
            big enough. On the other hand, bigger cycles consume more
            memory.
        '''
        self.delta = 10000
        self.data1 = None
        self.data2 = None
        self.final = []
        self.matches = 0
        self.nomatches = 0
    
    def reset_range(self):
        self.data1 = None
        self.data2 = None
        self.final = []
    
    def debug(self):
        f = '[DicExtractor] plugins.multitran.extractor.Compare.debug'
        if self.Success:
            data = objs.get_db().fetch_range(objs.db.table3,1,1000)
            if data:
                artnos = []
                subjects1 = []
                subjects2 = []
                subjects3 = []
                phrases1 = []
                phrases2 = []
                for row in data:
                    artnos.append(row[0])
                    subjects1.append(row[1])
                    subjects2.append(row[2])
                    subjects3.append(row[3])
                    phrases1.append(row[4])
                    phrases2.append(row[5])
                iterable = [artnos,subjects1,subjects2,subjects3
                           ,phrases1,phrases2
                           ]
                headers = ('ARTNO','SUBJ1','SUBJ2','SUBJ3','PHRASE1'
                          ,'PHRASE2'
                          )
                mes = sh.FastTable (iterable = iterable
                                   ,headers  = headers
                                   ,maxrow   = 50
                                   ).run()
                sh.com.run_fast_debug(mes)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def dump(self):
        f = '[DicExtractor] plugins.multitran.extractor.Compare.dump'
        if self.Success:
            if self.final:
                for row in self.final:
                    objs.get_db().add_final(row)
                objs.db.save()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def compare(self):
        f = '[DicExtractor] plugins.multitran.extractor.Compare.compare'
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
        self.debug()
    
    def get_max(self):
        f = '[DicExtractor] plugins.multitran.extractor.Compare.get_max'
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
        f = '[DicExtractor] plugins.multitran.extractor.Compare.set_ranges'
        if self.Success:
            ranges = com.calc_ranges(self.max_,self.delta)
            if ranges:
                for range_ in ranges:
                    self.reset_range()
                    self.data1 = objs.get_db().fetch_range(objs.db.table1,range_[0],range_[1])
                    self.data2 = objs.db.fetch_range(objs.db.table2,range_[0],range_[1])
                    self.compare()
                    self.dump()
                mes = _('Pairs in total/with matches/without matches:')
                sub = '{}/{}/{}'.format (self.matches + self.nomatches
                                        ,self.matches,self.nomatches
                                        )
                mes += '\n' + sub
                sh.objs.get_mes(f,mes).show_debug()
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class DB:

    def __init__(self,path):
        self.set_values()
        self.path = path
        self.connect()
        self.create()
    
    def create(self):
        self.create_table(self.table1)
        self.create_table(self.table2)
        self.create_final()
    
    def set_values(self):
        self.Success = True
        self.path = ''
        self.db = self.dbc = None
        self.table1 = 'LANG1'
        self.table2 = 'LANG2'
        self.table3 = 'LANG12'
    
    def get_max_artno(self,table):
        f = '[DicExtractor] plugins.multitran.extractor.DB.get_max_artno'
        if self.Success:
            query = 'select max(ARTNO) from {}'.format(table)
            self.dbc.execute(query)
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.cancel(f)
    
    def fetch_range(self,table,min_,max_):
        f = '[DicExtractor] plugins.multitran.extractor.DB.fetch_range'
        if self.Success:
            subquery = 'select * from {} where ARTNO >= ? \
                        and ARTNO <= ? order by ARTNO'
            query = subquery.format(table)
            self.dbc.execute(query,(min_,max_,))
            return self.dbc.fetchall()
        else:
            sh.com.cancel(f)
    
    def print (self,table='LANG1'
              ,maxrow=50,maxrows=1000
              ):
        f = '[DicExtractor] plugins.multitran.extractor.DB.print'
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
    
    def add_final(self,data):
        f = '[DicExtractor] plugins.multitran.extractor.DB.add_final'
        if self.Success:
            try:
                query = 'insert into {} values (?,?,?,?,?,?)'
                query = query.format(self.table3)
                self.dbc.execute(query,data)
                return True
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def add(self,data,lang=1):
        f = '[DicExtractor] plugins.multitran.extractor.DB.add'
        if self.Success:
            if lang == 1:
                table = self.table1
            else:
                table = self.table2
            try:
                query = 'insert into {} values (?,?,?,?,?)'
                query = query.format(table)
                self.dbc.execute(query,data)
                return True
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = '[DicExtractor] plugins.multitran.extractor.DB.save'
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
        f = '[DicExtractor] plugins.multitran.extractor.DB.clear'
        tables = [self.table1,self.table2,self.table3]
        mes = _('Delete all records from {}')
        mes = mes.format(', '.join(tables))
        sh.objs.get_mes(f,mes,True).show_warning()
        query = 'delete from {}'
        self.dbc.execute(query.format(self.table1))
        self.dbc.execute(query.format(self.table2))
        self.dbc.execute(query.format(self.table3))
        #TODO: vacuumize
    
    def create_final(self):
        f = '[DicExtractor] plugins.multitran.extractor.DB.create_final'
        if self.Success:
            try:
                query = 'create table if not exists {} (\
                         ARTNO    integer \
                        ,SUBJECT1 integer \
                        ,SUBJECT2 integer \
                        ,SUBJECT3 integer \
                        ,PHRASE1  text \
                        ,PHRASE2  text \
                                                       )'
                query = query.format(self.table3)
                self.dbc.execute(query)
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_table(self,lang):
        f = '[DicExtractor] plugins.multitran.extractor.DB.create_table'
        if self.Success:
            try:
                query = 'create table if not exists {} (\
                         ARTNO    integer \
                        ,SUBJECT1 integer \
                        ,SUBJECT2 integer \
                        ,SUBJECT3 integer \
                        ,PHRASE   text \
                                                       )'
                query = query.format(lang)
                self.dbc.execute(query)
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[DicExtractor] plugins.multitran.extractor.DB.close'
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
        f = '[DicExtractor] plugins.multitran.extractor.DB.connect'
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
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.__init__'
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
        # Number of 16K pages to process
        self.delta = 1000 # Buffer: at least 32M for both languages
    
    def report(self):
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.report'
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
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.debug'
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
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.set_phrases'
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
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.parse_typein'
        if self.Success:
            self.iparse = gt.Parser(file)
            self.iparse.parsel_loop(start_page,end_page)
            self.Success = self.iparse.Success
        else:
            sh.com.cancel(f)
    
    def translate(self,pattern):
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.translate'
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
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.dump'
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
                           ,self.phrases[i]
                           ,
                           )
                    if not objs.get_db().add(data,lang):
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
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.run_lang'
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
    
    def run_loop(self,end_page=100000000):
        f = '[DicExtractor] plugins.multitran.extractor.Extractor.run_loop'
        if self.Success:
            #cur
            #end_page = min(end_page,len(self.iparse.lpages))
            ranges = com.calc_ranges(end_page,self.delta)
            if ranges:
                for range_ in ranges:
                    self.run_cycle (lang       = 1
                                   ,start_page = range_[0]
                                   ,end_page   = range_[1]
                                   )
                    self.run_cycle (lang       = 2
                                   ,start_page = range_[0]
                                   ,end_page   = range_[1]
                                   )
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self,end_page=100000000):
        start_page = 0
        sh.STOP_MES = True
        objs.get_db().clear()
        objs.db.save()
        self.run_loop(end_page)
        sh.STOP_MES = False
        self.report()
        #objs.get_db().print('LANG1')
        #objs.db.print('LANG2')



class Objects:
    
    def __init__(self):
        self.db = None
    
    def get_db(self):
        if self.db is None:
            path = sh.Home('DicExtractor').add_config('extract.db')
            self.db = DB(path)
        return self.db


objs = Objects()
com = Commands()


if __name__ == '__main__':
    f = '[DicExtractor] plugins.multitran.extractor.__main__'
    gt.PATH = sh.Home('DicExtractor').get_conf_dir()
    gt.DEBUG = False
    gt.objs.get_files().reset()
    #Extractor().run()
    objs.get_db().print('LANG1')
    objs.db.print('LANG2')
    gt.objs.files.close()
    objs.get_db().close()
