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
    iparse = gt.Parser(gt.objs.get_files().iwalker.get_stems1())
    iparse.run_reader(557059,561358)
    iparse.parse()
    timer.end()
    iparse.debug(75)
