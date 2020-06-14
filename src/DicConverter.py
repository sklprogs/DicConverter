#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

import gui as gi
import plugins.multitran.extractor as mx
import plugins.lingvo.extractor as lx


class Menu:
    
    def __init__(self):
        self.gui = gi.Menu()
        self.set_bindings()
    
    def run_multitran(self,event=None):
        mx.Runner().run()
    
    def run_lingvo(self,event=None):
        lx.Runner().run()
    
    def set_bindings(self):
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
        self.gui.btn_mlt.action = self.run_multitran
        self.gui.btn_lgv.action = self.run_lingvo
        self.gui.btn_cls.action = self.close
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()


if __name__ == '__main__':
    f = '[DicConverter] DicConverter.__main__'
    lx.PATH = sh.Home('DicConverter').get_conf_dir()
    Menu().show()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
