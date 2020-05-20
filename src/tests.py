#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

import plugins.multitran.get       as mg
import plugins.multitran.extractor as mx
import plugins.multitran.tests     as mt


class Tests:
    
    def __init__(self):
        pass


if __name__ == '__main__':
    f = '[DicConverter] tests.__main__'
    mg.PATH = sh.Home('DicConverter').get_conf_dir()
    mg.DEBUG = True
    #mx.objs.get_db().print_not_found()
    #mx.objs.get_db().print_simple()
    #mx.objs.get_db().print_final()
    ''' Successful:
            tree wart
            cable drill
            close in
            due
            variable choke
        Failed to translate:
            cloud chamber
            training
            банда наёмных громил
            безусловно сходящаяся последовательность
            проходной разъём
            струиться
            убраться восвояси
            являться
            щебёночное покрытие c поливкой водой перед укаткой
    '''
    #print(mt.Tests().translate('training'))
    #mt.Tests().get_by_artnos()
    #mt.Tests().search()
    mt.Tests().search_like()
    #mx.objs.get_db().print(mx.objs.db.table2)
