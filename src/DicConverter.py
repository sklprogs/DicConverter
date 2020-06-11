#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

import plugins.multitran.extractor as mx
import plugins.lingvo.extractor as lx


if __name__ == '__main__':
    f = '[DicConverter] controller.__main__'
    lx.PATH = sh.Home('DicConverter').get_conf_dir()
    #mx.Runner().run()
    lx.Runner().run()
