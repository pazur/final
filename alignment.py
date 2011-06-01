import os.path
import tempfile

from Bio.Align.Applications import ClustalwCommandline
import Bio.Phylo

import inout
from settings import get_setting


COMPULSORY_SETTINGS = ('CLUSTALW_PATH',)

class Alignment(object):
    def __init__(self, input=None, *args, **kwargs):
        super(Alignment, self).__init__(*args, **kwargs)
        from settings import get_setting
        if input is None:
            self.input = get_setting('INPUT_FILE')
        else:
            self.input = input
    def run(self):
        exe = get_setting('CLUSTALW_PATH')
        tree_file = get_setting('CLUSTALW_NEWTREE', None)
        outfile = get_setting('CLUSTALW_OUTFILE', None)
        if tree_file is None:
            tree_file = create_tmp()
        if outfile is None:
            outfile = create_tmp()
        cline = ClustalwCommandline(exe, infile=self.input, newtree=tree_file)
        cline()
        cline = ClustalwCommandline(exe, infile=self.input, outfile=outfile)
        ###Fix "p.checker_function = lambda x: os.path.exists"
        param = [i for i,p in enumerate(cline.parameters) 
            if 'usetree' in p.names]
        cline.parameters[param[0]].checker_function = os.path.exists
        ###
        setattr(cline, 'usetree', tree_file)
        cline()
        return {'alignment': inout.AlignFileInput(file=outfile, format='clustal').read(),
            'tree': Bio.Phylo.read(tree_file, 'newick'),
        }

def create_tmp():
    file = tempfile.NamedTemporaryFile(delete=False)
    return file.name

def run(*args, **kwargs):
    return Alignment(*args, **kwargs).run()
