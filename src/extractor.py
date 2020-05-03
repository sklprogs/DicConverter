#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import get as gt


if __name__ == '__main__':
    f = '[MTExtractor] tests.__main__'
    gt.PATH = '/home/pete/.config/mclient/dics'
    gt.DEBUG = False
    timer = sh.Timer(f)
    timer.start()
    #get_stems1
    #get_typein1
    iparse = gt.Parser(gt.objs.get_files().iwalker.get_typein1())
    iparse.parsel_loop()
    timer.end()
    iparse.debug(75)
    mes = 'Chunks1: {}; chunks2: {}'.format (len(iparse.chunks1)
                                            ,len(iparse.chunks2)
                                            )
    sh.objs.get_mes(f,mes,True).show_debug()
