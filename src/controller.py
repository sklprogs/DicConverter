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
    mx.Extractor().run(20)
    mx.Compare().run()
    mx.objs.get_db().close()
