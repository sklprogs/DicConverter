#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

import plugins.multitran.get       as mg
import plugins.multitran.extractor as mx
import plugins.multitran.tests     as mt


if __name__ == '__main__':
    f = '[DicConverter] tests.__main__'
    #mx.objs.get_db().print_not_found()
    mg.PATH = sh.Home('DicConverter').get_conf_dir()
    mg.DEBUG = True
    file = mg.objs.get_files().iwalker.get_typein1()
    print('File:',file)
    mt.Binary(file).show_info()
