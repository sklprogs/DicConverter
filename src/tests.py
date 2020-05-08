#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

import plugins.multitran.extractor as mx


if __name__ == '__main__':
    f = '[DicConverter] tests.__main__'
    mx.objs.get_db().print_not_found()
