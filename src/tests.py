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
    #mg.DEBUG = True
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
    '''
    print(mt.Tests().translate('cloud chamber'))    
