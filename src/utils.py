#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import skl_shared.shared as sh
from skl_shared.localize import _

PATH = sh.Home('DicConverter').get_conf_dir()


class Commands:
    
    def delete_compiled(self):
        # Delete LSD/LOD files that have corresponding DSL files
        f = '[DicConverter] utils.Commands.delete_compiled'
        files = sh.Directory(PATH).get_subfiles()
        if files:
            for file in files:
                ipath = sh.Path(file)
                if ipath.get_ext_low() in ('.lsd','.lod'):
                    dirname = ipath.get_dirname()
                    fname = ipath.get_filename()
                    dsl = os.path.join(dirname,fname+'.dsl')
                    if os.path.exists(dsl):
                        sh.File(file).delete()
        else:
            sh.com.rep_empty(f)
    
    def get_lacking_dsl(self):
        # Get DSL files that do not have corresponding LOD/LSD files
        f = '[DicConverter] utils.Commands.get_lacking_dsl'
        lacking = []
        files = sh.Directory(PATH).get_subfiles()
        if files:
            for file in files:
                ipath = sh.Path(file)
                if ipath.get_ext_low() in ('.lsd','.lod'):
                    dirname = ipath.get_dirname()
                    fname = ipath.get_filename()
                    dsl = os.path.join(dirname,fname+'.dsl')
                    if not os.path.exists(dsl):
                        lacking.append(ipath.get_basename())
            if lacking:
                mes = _('Lacking DSL files ({} in total):')
                mes = mes.format(len(lacking))
                mes += '\n\n' + '\n'.join(lacking)
                sh.objs.get_mes(f,mes).show_info()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.rep_empty(f)


com = Commands()


if __name__ == '__main__':
    com.delete_compiled()
