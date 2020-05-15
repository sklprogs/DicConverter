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
    #mx.objs.get_db().print_not_found()
    #mx.objs.get_db().print_simple()
    mx.objs.get_db().print_final()
    #print(mt.Tests().translate('tree wart'))
    '''
    Failed to translate:
    cable drill
    close in
    cloud chamber
    due
    tree wart
    variable choke
    '''
