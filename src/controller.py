#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

import plugins.multitran.get as mg
import plugins.multitran.extractor as mx


if __name__ == '__main__':
    f = '[DicExtractor] controller.__main__'
    mg.PATH = sh.Home('DicExtractor').get_conf_dir()
    mg.DEBUG = False
    mg.objs.get_files().reset()
    #mx.Extractor().run()
    mx.objs.get_db().print('LANG1')
    mx.objs.db.print('LANG2')
    mg.objs.files.close()
    mx.objs.get_db().close()
