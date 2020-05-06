#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

import plugins.multitran.extractor as mx


if __name__ == '__main__':
    f = '[DicExtractor] controller.__main__'
    mx.Runner(end_page=10).run()
