#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

ICON = sh.objs.get_pdir().add ('..','resources'
                              ,'icon_64x64_DicConverter.gif'
                              )


class Menu:
    
    def __init__(self):
        self.set_gui()
    
    def set_gui(self):
        self.parent = sh.Top (title = _('Convert dictionaries:')
                             ,icon  = ICON
                             )
        self.widget = self.parent.widget
        self.set_buttons()
        self.set_bindings()
    
    def set_bindings(self):
        sh.com.bind (obj      = self.parent
                    ,bindings = '<Control-q>'
                    ,action   = self.close
                    )
        sh.com.bind (obj      = self.btn_mlt
                    ,bindings = '<Down>'
                    ,action   = self.btn_lgv.focus
                    )
        sh.com.bind (obj      = self.btn_lgv
                    ,bindings = '<Down>'
                    ,action   = self.btn_cls.focus
                    )
        sh.com.bind (obj      = self.btn_cls
                    ,bindings = '<Down>'
                    ,action   = self.btn_mlt.focus
                    )
        sh.com.bind (obj      = self.btn_mlt
                    ,bindings = '<Up>'
                    ,action   = self.btn_cls.focus
                    )
        sh.com.bind (obj      = self.btn_lgv
                    ,bindings = '<Up>'
                    ,action   = self.btn_mlt.focus
                    )
        sh.com.bind (obj      = self.btn_cls
                    ,bindings = '<Up>'
                    ,action   = self.btn_lgv.focus
                    )
    
    def set_buttons(self):
        self.btn_mlt = sh.Button (parent = self.parent
                                 ,text   = 'Multitran'
                                 ,side   = 'top'
                                 ,Focus  = True
                                 )
        self.btn_lgv = sh.Button (parent = self.parent
                                 ,text   = 'Lingvo'
                                 ,side   = 'top'
                                 )
        self.btn_cls = sh.Button (parent = self.parent
                                 ,text   = _('Quit')
                                 ,side   = 'top'
                                 )
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
        
