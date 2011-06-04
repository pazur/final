import os.path

from Bio.Align.Applications import ClustalwCommandline
import Bio.Phylo

import inout
from settings import get_setting
import settings_validator
from utils import create_tmp


COMPULSORY_SETTINGS = ('CLUSTALW_PATH',)
ARGUMENTS = (
    'input',        # Input file
    'sequences',    # list of input sequences
    'only_tree',    # boolean - if true - create only tree (without alignment)
)
RESULTS = (
    'tree',         # Bio.Phylo.Tree
    'tree_out',     # clustalw stdout (tree)
    'tree_err',     # clustalw errout (tree)
    'alignment',    # Multiple alignment
    'align_out',    # clustalw stdout (aligment)
    'align_err',    # clustalw errout (alignment)
)

class SettingsValidator(settings_validator.SettingsValidator):
    def validate_CLUSTALW_PATH(self, value):
        self.validate_file(value, 'CLUSTALW_PATH')

    def validate_CLUSTALW_NEWTREE(self, value):
        self.validate_string(value, 'CLUSTALW_NEWTREE')

    def validate_CLUSTALW_OUTFILE(self, value):
        self.validate_string(value, 'CLUSTALW_OUTFILE')


class Alignment(object):
    def __init__(self, input=None, sequences=None, only_tree=False, *args, **kwargs):
        super(Alignment, self).__init__(*args, **kwargs)
        from settings import get_setting
        if sequences is not None:
            input = create_tmp()
            inout.FileOutput(input).write(sequences)
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

def run(*args, **kwargs):
    return Alignment(*args, **kwargs).run()
