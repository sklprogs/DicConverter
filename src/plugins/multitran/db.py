#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import skl_shared.shared as sh
from skl_shared.localize import _


class DB:

    def __init__(self,path):
        self.set_values()
        self.path = path
        self.connect()
        self.create()
    
    def print_simple (self,table='LANG1'
                     ,maxrow=45,maxrows=1000
                     ):
        f = '[DicConverter] plugins.multitran.db.DB.print_simple'
        if self.Success:
            subquery = 'select ARTNO,SIMPLE,PHRASE from {} \
                        order by ARTNO,SIMPLE limit ?'
            query = subquery.format(table)
            self.dbc.execute(query,(maxrows,))
            data = self.dbc.fetchall()
            if data:
                headers = ('NO','ARTNO','SIMPLE','PHRASE')
                rows = []
                for i in range(len(data)):
                    row = [i+1,data[i][0],data[i][1],data[i][2]]
                    rows.append(row)
                mes = sh.FastTable (iterable = rows
                                   ,headers = headers
                                   ,maxrow = maxrow
                                   ,maxrows = maxrows
                                   ,Transpose = True
                                   ).run()
                sub = _('Table: {}').format(table)
                mes = sub + '\n\n' + mes
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def print_not_found (self,table='LANG1'
                        ,maxrow=50,maxrows=1000
                        ):
        f = '[DicConverter] plugins.multitran.db.DB.print_not_found'
        if self.Success:
            subquery = 'select ARTNO,SUBJECT1,SUBJECT2,SUBJECT3,PHRASE \
                        from {} where ARTNO = ? order by PHRASE limit ?'
            query = subquery.format(table)
            self.dbc.execute(query,(-1,maxrows,))
            data = self.dbc.fetchall()
            if data:
                headers = ('NO','ARTNO','SUBJECT1','SUBJECT2'
                          ,'SUBJECT3','PHRASE'
                          )
                rows = []
                for i in range(len(data)):
                    row = [i+1,data[i][0],data[i][1],data[i][2]
                          ,data[i][3],data[i][4]
                          ]
                    rows.append(row)
                mes = sh.FastTable (iterable = rows
                                   ,headers = headers
                                   ,maxrow = maxrow
                                   ,maxrows = maxrows
                                   ,Transpose = True
                                   ).run()
                sub = _('Table: {}').format(table)
                mes = sub + '\n\n' + mes
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
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
        f = '[DicConverter] plugins.multitran.db.DB.get_max_artno'
        if self.Success:
            query = 'select max(ARTNO) from {}'.format(table)
            self.dbc.execute(query)
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.cancel(f)
    
    def fetch_range(self,table,min_,max_):
        f = '[DicConverter] plugins.multitran.db.DB.fetch_range'
        if self.Success:
            subquery = 'select * from {} where ARTNO >= ? \
                        and ARTNO <= ? order by ARTNO'
            query = subquery.format(table)
            self.dbc.execute(query,(min_,max_,))
            return self.dbc.fetchall()
        else:
            sh.com.cancel(f)
    
    def print_final(self,maxrow=45,maxrows=1000):
        f = '[DicConverter] plugins.multitran.db.DB.print_final'
        if self.Success:
            subquery = 'select {} from {} order by ARTNO desc limit ?'
            query = subquery.format('ARTNO',self.table3)
            self.dbc.execute(query,(maxrows,))
            artnos = self.dbc.fetchall()
            if artnos:
                artnos = [artno[0] for artno in artnos]
            else:
                artnos = []
            
            query = subquery.format('SUBJECT1',self.table3)
            self.dbc.execute(query,(maxrows,))
            subjects = self.dbc.fetchall()
            if subjects:
                subjects = [subject[0] for subject in subjects]
            else:
                subjects = []
            
            query = subquery.format('PHRASE1',self.table3)
            self.dbc.execute(query,(maxrows,))
            phrases1 = self.dbc.fetchall()
            
            query = subquery.format('PHRASE2',self.table3)
            self.dbc.execute(query,(maxrows,))
            phrases2 = self.dbc.fetchall()
            
            if phrases1:
                phrases1 = [phrase[0] for phrase in phrases1]
            else:
                phrases1 = []
            
            if phrases2:
                phrases2 = [phrase[0] for phrase in phrases2]
            else:
                phrases2 = []
            
            headers = ('NO','ARTNO','SUBJECT','PHRASE1','PHRASE2')
            nos = [i + 1 for i in range(len(subjects))]
            iterable = [nos,artnos,subjects,phrases1,phrases2]
            mes = sh.FastTable (iterable = iterable
                               ,headers = headers
                               ,maxrow = maxrow
                               ,maxrows = maxrows
                               ).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def print (self,table='LANG1'
              ,maxrow=50,maxrows=1000
              ):
        f = '[DicConverter] plugins.multitran.db.DB.print'
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
                               ,headers = headers
                               ,maxrow = maxrow
                               ,maxrows = maxrows
                               ).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def add_final(self,data):
        f = '[DicConverter] plugins.multitran.db.DB.add_final'
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
        f = '[DicConverter] plugins.multitran.db.DB.add'
        if self.Success:
            if lang == 1:
                table = self.table1
            else:
                table = self.table2
            try:
                query = 'insert into {} values (?,?,?,?,?,?)'
                query = query.format(table)
                self.dbc.execute(query,data)
                return True
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = '[DicConverter] plugins.multitran.db.DB.save'
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
        f = '[DicConverter] plugins.multitran.db.DB.clear'
        if self.Success:
            tables = [self.table1,self.table2,self.table3]
            mes = _('Delete all records from {}')
            mes = mes.format(', '.join(tables))
            sh.objs.get_mes(f,mes,True).show_warning()
            query = 'delete from {}'
            try:
                self.dbc.execute(query.format(self.table1))
                self.dbc.execute(query.format(self.table2))
                self.dbc.execute(query.format(self.table3))
            except Exception as e:
                self.fail(f,e)
            #TODO: vacuumize
        else:
            sh.com.cancel(f)
    
    def create_final(self):
        f = '[DicConverter] plugins.multitran.db.DB.create_final'
        if self.Success:
            query = 'create table if not exists {} (\
                     ARTNO    integer \
                    ,SUBJECT1 integer \
                    ,SUBJECT2 integer \
                    ,SUBJECT3 integer \
                    ,PHRASE1  text \
                    ,PHRASE2  text \
                                                   )'
            query = query.format(self.table3)
            try:
                self.dbc.execute(query)
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def create_table(self,lang):
        f = '[DicConverter] plugins.multitran.db.DB.create_table'
        if self.Success:
            # 6 columns for now
            query = 'create table if not exists {} (\
                     ARTNO    integer \
                    ,SUBJECT1 integer \
                    ,SUBJECT2 integer \
                    ,SUBJECT3 integer \
                    ,SIMPLE   text \
                    ,PHRASE   text \
                                                   )'
            query = query.format(lang)
            try:
                self.dbc.execute(query)
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[DicConverter] plugins.multitran.db.DB.close'
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
        f = '[DicConverter] plugins.multitran.db.DB.connect'
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
