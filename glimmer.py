import re
import subprocess
import inout
from settings import get_setting
from utils import create_tmp

COMPULSORY_SETTINGS = ('GLIMMER_PATH',)

ARGUMENTS = (
    'sequence',
    'icm_file',
    'extra',
)
RESULTS = (
    'genes',
    'glimmer_output',
    'glimmer_exit_code',
)

class Glimmer(object):
    def __init__(self, icm_file = None, sequence = None, extra = None, *args, **kwargs):
        super(Glimmer, self).__init__(*args, **kwargs)
        if sequence is None:
            sequence = inout.SingleSequenceFileInput().read()
        if icm_file is None:
            icm_file = get_setting('ICM_FILE')
        if extra is None:
            extra = {}
        self.sequence = sequence
        self.icm_file = icm_file
        self.extra = extra

    def run_glimmer(self):
        input_file = create_tmp()
        output_file = create_tmp()
        inout.FileOutput(input_file).write(self.sequence)
        exit_code = subprocess.call([get_setting('GLIMMER_PATH'), input_file, self.icm_file, output_file])
        return exit_code, output_file

    def read_genes(self, glimmer_output_file):
        for (start, end) in self.get_positions(glimmer_output_file):
            if end < start:
                start, end = end, start
            yield self.sequence[start - 1:end]

    def get_positions(self, glimmer_output_file):
        with open(glimmer_output_file) as f:
            for line in f:
                match = re.search(r".{10}\s+\d+\s+(?P<start>\d+)\s+(?P<end>\d+)", line)
                if match:
                    yield (int(match.groupdict()['start']), int(match.groupdict()['end']))

    def run(self):
        glimmer_exit_code, glimmer_output = self.run_glimmer()
        genes = self.read_genes(glimmer_output)
        return {
            'genes': genes,
            'glimmer_output': glimmer_output,
            'glimmer_exit_code': glimmer_exit_code,
        }

def run(*args, **kwargs):
    return Glimmer(*args, **kwargs).run()