from Bio.Align.Applications import ClustalwCommandline

import inout
import os.path

COMPULSORY_SETTINGS = ('CLUSTALW_PATH',)

class Alignment(object):
    def __init__(self, input=None):
        from settings import get_setting
        if input is None:
            self.input = get_setting('INPUT_FILE')
        else:
            self.input = input
    def run(self):
        from settings import get_setting
        exe = get_setting('CLUSTALW_PATH')
        tree_file = 'tree.txt'
        cline = ClustalwCommandline(exe, infile=self.input, newtree=tree_file)
        cline()
        cline = ClustalwCommandline(exe, infile=self.input, outfile='out.txt')
        ###Fix "p.checker_function = lambda x: os.path.exists"
        param = [i for i,p in enumerate(cline.parameters) 
            if 'usetree' in p.names]
        cline.parameters[param[0]].checker_function = os.path.exists
        ###
        setattr(cline, 'usetree', tree_file)
        cline()

def run(*args, **kwargs):
    return Alignment(*args, **kwargs).run()

def write(output):
    pass
