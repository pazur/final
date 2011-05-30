from Bio.Align.Applications import ClustalwCommandline

import inout

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
        cline = ClustalwCommandline(exe, infile=self.input, outfile='temp_file.txt')
        stdout, stderr = cline()


def run(*args, **kwargs):
    return Alignment(*args, **kwargs).run()

def write(output):
    pass