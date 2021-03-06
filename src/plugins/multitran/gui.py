#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

ICON = sh.objs.get_pdir().add ('..','resources'
                              ,'icon_64x64_DicConverter.gif'
                              )


class ProgressBar(sh.ProgressBar):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.add()
    
    def set_text(self,text=None):
        if text is None:
            text = _('Read single records')
        self.item.label.set_text(text)
    
    def update(self,percent):
        self.item.widget['value'] = percent
        # This is required to fill the progress bar on-the-fly
        sh.objs.get_root().update_idle()
