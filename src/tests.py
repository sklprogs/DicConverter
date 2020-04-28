#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import struct
import get               as gt
import skl_shared.shared as sh
from skl_shared.localize import _


class Commands:
    
    def swap_langs(self):
        gt.LANG1, gt.LANG2 = gt.LANG2, gt.LANG1
        gt.objs.get_files().reset()



class Xor(gt.Xor):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def debug(self):
        nos = [i for i in range(256)]

        ''' This is basically a listing of 'cp1251' encoding with
            control characters replaced with 'None'.
        '''
        syms = [None for i in range(33)]
        syms += ['!','"','#','$','%','&',"'",'(',')','*','+',','
                ,'-','.','/','0','1','2','3','4','5','6','7','8'
                ,'9',':',';','<','=','>','?','@','A','B','C','D'
                ,'E','F','G','H','I','J','K','L','M','N','O','P'
                ,'Q','R','S','T','U','V','W','X','Y','Z','[','\\'
                ,']','^','_','`','a','b','c','d','e','f','g','h'
                ,'i','j','k','l','m','n','o','p','q','r','s','t'
                ,'u','v','w','x','y','z','{','|','}','~',None,'Ђ'
                ,'Ѓ','‚','ѓ','„','…','†','‡','€','‰','Љ','‹','Њ'
                ,'Ќ','Ћ','Џ','ђ','‘','’','“','”','•','–','—'
                ,None,'™','љ','›','њ','ќ','ћ','џ',None,'Ў','ў'
                ,'Ћ','¤','Ґ','¦','§','Ё','©','Є','«','¬',None
                ,'®','Ї','°','±','І','і','ґ','µ','¶','·','ё'
                ,'№','є','»','ј','Ѕ','ѕ','ї','А','Б','В','Г'
                ,'Д','Е','Ж','З','И','Й','К','Л','М','Н','О'
                ,'П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ'
                ,'Ъ','Ы','Ь','Э','Ю','Я','а','б','в','г','д'
                ,'е','ж','з','и','й','к','л','м','н','о','п'
                ,'р','с','т','у','ф','х','ц','ч','ш','щ','ъ'
                ,'ы','ь','э','ю','я'
                ]

        headers = ('NO','TRANSL','OFFSET')
        iterable = [nos,syms,self.vectors]
        mes = sh.FastTable (headers  = headers
                           ,iterable = iterable
                           ).run()
        sh.com.run_fast_debug(mes)



class Ending(gt.Ending):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def debug(self):
        f = '[MTExtractor] tests.Ending.debug'
        if self.Success:
            ends     = list(self.ends)
            ends     = [str(end) for end in ends]
            headers  = ('#','ENDINGS')
            iterable = (self.nos,ends)
            mes = sh.FastTable (iterable = iterable
                               ,headers  = headers
                               ).run()
            sub = _('File: "{}"').format(self.file)
            mes = sub + '\n\n' + mes
            sh.com.run_fast_debug(mes)
        else:
            sh.com.cancel(f)



class Subject(gt.Subject):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def debug(self):
        f = '[MTExtractor] tests.Subject.debug'
        if self.Success:
            headers  = ('#','FULL (1)','ABBR (1)','FULL (2)','ABBR (2)')
            iterable = (self.dic_nos,self.en_dicf
                       ,self.en_dic,self.ru_dicf
                       ,self.ru_dic
                       )
            mes = sh.FastTable (headers  = headers
                               ,iterable = iterable
                               ).run()
            sub = _('File: "{}"').format(self.file)
            mes = sub + '\n\n' + mes
            sh.com.run_fast_debug(mes)
        else:
            sh.com.cancel(f)



class Binary(gt.Binary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def get_max_limits(self,page_no):
        ''' Return positions of a page based on a block size.
            #NOTE: Seems that 'get.Binary.get_page_limits' which
                   returns a narrower range works fine, so I use
                   the present function for testing purposes only.
        '''
        f = '[MTExtractor] tests.Binary.get_max_limits'
        if self.Success:
            if page_no is None or not self.get_block_size():
                sh.com.rep_empty(f)
            else:
                mes = _('Page #: {}').format(page_no)
                sh.objs.get_mes(f,mes,True).show_debug()
                pos1 = page_no * self.bsize
                pos2 = pos1 + self.bsize
                sub1 = sh.com.set_figure_commas(pos1)
                sub2 = sh.com.set_figure_commas(pos2)
                mes  = _('Page limits: [{}:{}]').format(sub1,sub2)
                sh.objs.get_mes(f,mes,True).show_debug()
                return(pos1,pos2)
        else:
            sh.com.cancel(f)
    
    def show_info(self):
        f = '[MTExtractor] tests.Binary.show_info'
        self.get_block_size()
        self.get_file_size()
        self.get_pages()
        if self.Success:
            iwrite = io.StringIO()
            mes = _('File: {}').format(self.file)
            iwrite.write(mes)
            iwrite.write('\n')
            size = sh.com.get_human_size(self.fsize)
            mes  = _('File size: {}').format(size)
            iwrite.write(mes)
            iwrite.write('\n')
            size = sh.com.set_figure_commas(self.bsize)
            mes  = _('Block size: {}').format(size)
            iwrite.write(mes)
            iwrite.write('\n\n')
            mes = _('Pages:')
            iwrite.write(mes)
            iwrite.write('\n')
            nos    = []
            types  = []
            poses1 = []
            poses2 = []
            sizes  = []
            for i in range(len(self.pages)):
                # Page #0 is actually an M area
                nos.append(i+1)
                if self.pages[i] in self.upages:
                    types.append('U')
                elif self.pages[i] in self.lpages:
                    types.append('L')
                elif self.pages[i] in self.zpages:
                    types.append('Z')
                else:
                    types.append(_('N/A'))
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes).show_error()
                # The first page is actually an M area
                poses = self.get_page_limits(i+1)
                if poses:
                    poses1.append(sh.com.set_figure_commas(poses[0]))
                    poses2.append(sh.com.set_figure_commas(poses[1]))
                    delta = poses[1] - poses[0]
                    sizes.append(sh.com.set_figure_commas(delta))
                else:
                    sh.com.rep_empty(f)
                    poses1.append(_('N/A'))
                    poses2.append(_('N/A'))
                    sizes.append(_('N/A'))
            headers  = ('#','TYPE','POS1','POS2','SIZE')
            iterable = [nos,types,poses1,poses2,sizes]
            mes = sh.FastTable (headers  = headers
                               ,iterable = iterable
                               ).run()
            iwrite.write(mes)
            iwrite.write('\n')
            mes = iwrite.getvalue()
            iwrite.close()
            sh.com.run_fast_debug(mes)
        else:
            sh.com.cancel(f)



class Tests:
    
    def get_shift(self):
        # o -> q, 111 -> 113: -4
        # n -> q, 110 -> 113: -14
        # ъ -> я, 250 -> 255: 246
        pos1 = 112
        pos2 = 114
        gt.Xor().get_shift(pos1,pos2)
    
    def xor(self):
        # Expected: b'p', pos: 112, +26 => b'\x8a', 138 (-2)
        # Expected: b'p' ->, pos: 112, offset: -67 -> b'-', pos: 45
        pattern = 'p'
        coded = bytes(pattern,gt.CODING)
        gt.Xor().xor(coded)
    
    def dexor(self):
        # 'petroleum'
        chunk = b'-\x88\xfb\x89j\xc5\xd1\x82x'
        dex = gt.Dexor()
        dex.dexor(byte,start=-186)
    
    def suggest(self):
        #pattern = 'acid'
        pattern  = 'кислот'
        com.swap_langs()
        timer = sh.Timer()
        timer.start()
        gt.objs.get_files().get_typein1().search(pattern)
        timer.end()
    
    def get_speech(self,pattern):
        ''' 'absolut'  -> 176     -> 32
            'absolute' -> 31,123  -> 2 ('absolutely')
            'absolute' -> 188,481 -> 67
            'measurement': [916, 3, 67, 80760, 20, 32, 223439, 3, 66]
        '''
        get = gt.Get(pattern)
        get.run()
        stemnos = get.stemnos
        stemnos = [gt.com.unpack(no) for no in stemnos]
        stemnos = [sh.com.set_figure_commas(no) for no in stemnos]
        sh.objs.get_mes(f,stemnos,True).show_debug()
        mes = '"{};{}"'.format(get.speech,get.spabbr)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def run_ending(self):
        subj = Ending(gt.objs.get_files().iwalker.get_ending())
        subj.debug()
    
    def run_subject(self):
        subj = Subject(gt.objs.get_files().iwalker.get_subject())
        subj.debug()
    
    def _parse_upage(self,file):
        upage = UPage(file)
        upage.get_parts()
        upage.debug()
    
    def searchu_article(self):
        #pattern = b'\x00'
        #pattern = b'\x01\x02\x03'
        #pattern = b'\x02\x01\x03'
        #pattern = b'A'
        #pattern = b'\x02'
        #pattern = b'\x03'
        #pattern = b'\x04'
        #pattern = b':'
        #pattern = b'\xfc'
        pattern  = b'\xfd'
        upage = UPage(gt.objs.get_files().iwalker.get_article())
        upage.get_parts()
        upage.searchu(pattern)
        #upage.debug()
    
    def parse_upage(self):
        file = gt.objs.get_files().iwalker.get_stems1()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_stems2()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_glue1()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_glue2()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_article()
        self._parse_upage(file)
    
    def searchu_glue(self):
        #pattern = b'\x1b-\x00'
        pattern  = b'\x00'
        upage = UPage(gt.objs.get_files().iwalker.get_glue1())
        upage.get_parts()
        upage.searchu(pattern)
        #upage.debug()
    
    def get_upage_stems(self):
        upage = UPage(gt.objs.get_files().iwalker.get_stems1())
        upage.get_parts()
        part1  = list(upage.part1)
        part2  = list(upage.part2)
        part1d = [item.decode(gt.CODING,'replace') for item in part1]
        part2l = []
        for i in range(len(part2)):
            if part2[i]:
                unpacked = struct.unpack('<h',part2[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part2l.append(unpacked)
            else:
                part2l.append('""')
        header = ('CHUNK1','CP1251','CHUNK2','<h')
        data   = [part1,part1d,part2,part2l]
        mes = sh.FastTable (headers  = header
                           ,iterable = data
                           ,sep      = 3 * ' '
                           ).run()
        sh.com.run_fast_debug(mes)
    
    def get_upage_glue(self):
        upage = UPage(gt.objs.get_files().iwalker.get_glue1())
        upage.get_parts()
        part1  = list(upage.part1)
        part2  = list(upage.part2)
        part1l = []
        for i in range(len(part1)):
            if part1[i]:
                unpacked = struct.unpack('<b',part1[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part1l.append(unpacked)
            else:
                part1l.append('""')
        part2l = []
        for i in range(len(part2)):
            if part2[i]:
                unpacked = struct.unpack('<h',part2[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part2l.append(unpacked)
            else:
                part2l.append('""')
        header = ('CHUNK1','<b','CHUNK2','<h')
        data   = [part1,part1l,part2,part2l]
        mes = sh.FastTable (headers  = header
                           ,iterable = data
                           ,sep      = 3 * ' '
                           ).run()
        sh.com.run_fast_debug(mes)
    
    def searchu_stems(self):
        f = '[MTExtractor] tests.Tests.searchu_stems'
        timer = sh.Timer(f)
        timer.start()
        #pattern = b'wol'
        #pattern = b'zero'
        #pattern = b'wi'
        #pattern = b'wifi'
        #pattern = b'willing'
        #pattern = b'vh'
        #pattern = b'ace'
        #pattern = b'a'
        #pattern = b'algorithm'
        #pattern = b'wol'
        #pattern = b'acf'
        #pattern = b'volume'
        pattern = b'abatement'
        
        upage = UPage(gt.objs.get_files().iwalker.get_stems1())
        upage.searchu(pattern)
        print('---------------------------------------------------')
        #pattern = 'уборка'
        #pattern = 'эт'
        #pattern = 'аж'
        #pattern = 'ажиотаж'
        #pattern = 'аккордеон'
        #pattern = 'ан'
        #pattern = 'анорексия'
        #pattern = 'ас'
        #pattern = 'асс'
        #pattern = 'язык'
        #pattern = 'этот'
        #pattern = 'железобетонный принцип'
        #pattern = 'з'
        #pattern = 'задеть'
        #pattern = 'зашуганный'
        pattern  = 'звезда'
        pattern  = bytes(pattern,gt.CODING)
        com.swap_langs()
        # Since we swap languages, the needed stems will always be #1
        upage = UPage(gt.objs.get_files().iwalker.get_stems1())
        upage.searchu(pattern)
        timer.end()
        #upage.debug()
    
    def translate_pair(self):
        self.translate('abasin')
        com.swap_langs()
        # 'factorage', 'sack' # 2 terms
        self.translate('уборка') # has a comment
    
    def translate_many(self):
        f = '[MTExtractor] tests.Tests.translate_many'
        ''' MISSING IN MT DEMO:
            'преобразование случайной величины X, имеющей асимметричное распределение, в нормально распределённую величину Z'
        '''
        timer = sh.Timer()
        timer.start()
        sh.STOP_MES = True
        en_patterns = ['A & E'
                      ,'a posteriori'
                      ,'abasin'
                      ,'abatement of purchase price'
                      ,'abatement of tax'
                      ,'abbrmate'
                      ,'absolute measurements'
                      ,'acceleration measured in G'
                      ,'acceleration spectral density'
                      ,'ashlar line'
                      ,'baby fish'
                      ,'Bachelor of Vocational Education'
                      ,'calcium gallium germanium garnet'
                      ,'daily reports notice'
                      ,'deaf as an adder'
                      ,'eristic'
                      ,'habitable room'
                      ,'he has not a sou'
                      ,'Kapteyn transformation'
                      ,'law and equity'
                      ,'loadable system'
                      ,'palletbox'
                      ,'sack duty'
                      ,'work'
                      ,'World Union of Catholic Teachers'
                      ,'Zebra time'
                      ]
        ru_patterns = ['абонентское устройство для совместной передачи речи и данных'
                      ,'абсолютный способ измерения'
                      ,'Всемирный союз преподавателей-католиков'
                      ,'курс занятий для студентов последнего курса'
                      ,'с большой точностью'
                      ,'уборка'
                      ,'у него нет ни гроша'
                      ,'ячейка решётки'
                      ,'ящичный поддон'
                      ]
        failed = 0
        total  = len(en_patterns) + len(ru_patterns)
        for pattern in en_patterns:
            if not self.translate(pattern):
                failed += 1
        com.swap_langs()
        for pattern in ru_patterns:
            if not self.translate(pattern):
                failed += 1
        sh.STOP_MES = False
        timer.end()
        messages = []
        mes = _('Total: {}').format(total)
        messages.append(mes)
        mes = _('Successful: {}').format(total-failed)
        messages.append(mes)
        mes = _('Failed: {}').format(failed)
        messages.append(mes)
        mes = '\n' + '\n'.join(messages)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def translate(self,pattern):
        f = '[MTExtractor] tests.Tests.translate'
        timer = sh.Timer(f)
        timer.start()
        result = gt.Get(pattern).run()
        sh.objs.get_mes(f,result,True).show_debug()
        timer.end()
        return result



class UPage(gt.UPage):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def debug(self):
        f = '[MTExtractor] tests.UPage.debug'
        if self.Success:
            if self.file in (gt.objs.get_files().iwalker.get_stems1()
                            ,gt.objs.files.iwalker.get_stems2()
                            ):
                self.debug_stems()
            else:
                self.debug_glue()
        else:
            sh.com.cancel(f)
    
    def debug_glue(self):
        f = '[MTExtractor] tests.UPage.debug_glue'
        if self.Success:
            if self.part2:
                part1 = [gt.com.get_string(chunk) \
                         for chunk in self.part1
                        ]
                part2 = [struct.unpack('<h',chunk)[0] \
                         for chunk in self.part2
                        ]
                mes = sh.FastTable (headers  = ('STEM','PAGEREF')
                                   ,iterable = (part1,part2)
                                   ,sep      = 3 * ' '
                                   ).run()
                if mes:
                    mes = _('File: {}').format(self.file) + '\n\n' + mes
                    sh.com.run_fast_debug(mes)
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def debug_stems(self):
        f = '[MTExtractor] tests.UPage.debug_stems'
        if self.Success:
            if self.part2:
                part1 = [chunk.decode(gt.CODING,'ignore') \
                         for chunk in self.part1
                        ]
                part2 = [struct.unpack('<h',chunk)[0] \
                         for chunk in self.part2
                        ]
                mes = sh.FastTable (headers  = ('STEM','PAGEREF')
                                   ,iterable = (part1,part2)
                                   ,sep      = 3 * ' '
                                   ).run()
                if mes:
                    mes = _('File: {}').format(self.file) + '\n\n' + mes
                    sh.com.run_fast_debug(mes)
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)


com = Commands()


if __name__ == '__main__':
    f = '[MTExtractor] tests.__main__'
    gt.PATH = '/home/pete/.config/mclient/dics'
    ''' Currently failing translations:
        "work"
        "совковая лопата с суживающимся полотном с прямолинейной кромкой"
        "собирать и содержать в определённом месте потерявшихся домашних животных или автомобили"
    '''
    #Tests().get_speech('DARE')
    #Tests().translate('DARE')
    #Binary(gt.objs.get_files().iwalker.get_glue1()).show_info()
    gt.DEBUG = True
    # creeping Coxsackies
    pattern = 'rabal'
    iget = gt.Get(pattern)
    iget.check()
    iget.strip()
    gt.objs.get_files().reset()
    iget.get_stems()
    iget.get_combos()
    iget.set_speech()
    mes = iget.search()
    sh.objs.get_mes(f,mes,True).show_debug()
