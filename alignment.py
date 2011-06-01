import os.path
import tempfile

from Bio.Align.Applications import ClustalwCommandline
import Bio.Phylo

import inout
from settings import get_setting


COMPULSORY_SETTINGS = ('CLUSTALW_PATH',)

class Alignment(object):
    def __init__(self, input=None, only_tree=False, *args, **kwargs):
        super(Alignment, self).__init__(*args, **kwargs)
        from settings import get_setting
        if input is None:
            self.input = get_setting('INPUT_FILE')
        else:
            self.input = input
        self.only_tree = only_tree

    def run(self):
        exe = get_setting('CLUSTALW_PATH')
        tree_file = get_setting('CLUSTALW_NEWTREE', None)
        if tree_file is None:
            tree_file = create_tmp()
        cline = ClustalwCommandline(exe, infile=self.input, newtree=tree_file)
        build_tree_out, build_tree_err = cline()
        result = {
            'tree': Bio.Phylo.read(tree_file, 'newick'),
            'tree_out': build_tree_out,
            'tree_err': build_tree_err,
        }
        if self.only_tree:
            return result

        outfile = get_setting('CLUSTALW_OUTFILE', None)
        if outfile is None:
            outfile = create_tmp()
        cline = ClustalwCommandline(exe, infile=self.input, outfile=outfile)
        ###Fix "p.checker_function = lambda x: os.path.exists"
        param = [i for i,p in enumerate(cline.parameters) 
            if 'usetree' in p.names]
        cline.parameters[param[0]].checker_function = os.path.exists
        ###
        setattr(cline, 'usetree', tree_file)
        align_out, align_err = cline()
        result.update({
            'align_out': align_out,
            'align_err': align_err,
            'alignment': inout.AlignFileInput(file=outfile, format='clustal').read(),
        })
        return result

def create_tmp():
    file = tempfile.NamedTemporaryFile(delete=False)
    return file.name

def run(*args, **kwargs):
    return Alignment(*args, **kwargs).run()
