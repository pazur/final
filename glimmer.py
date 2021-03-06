import re
import subprocess
import inout
from settings import get_file
from utils import create_tmp

COMPULSORY_SETTINGS = ('GLIMMER_PATH',)

ARGUMENTS = (
    'sequence',
    'icm_file',
    'extra',
)
RESULTS = (
    'genes',
    'glimmer_details',
    'glimmer_exit_code',
    'glimmer_predict'
)

class Glimmer(object):
    def __init__(self, icm_file = None, sequence = None, extra = None, *args, **kwargs):
        super(Glimmer, self).__init__(*args, **kwargs)
        if sequence is None:
            sequence = inout.SingleSequenceFileInput().read()
        if icm_file is None:
            icm_file = get_file('ICM_FILE')
        if extra is None:
            extra = []
        self.sequence = sequence
        self.icm_file = icm_file
        self.extra = list(extra)

    def run_glimmer(self):
        input_file = create_tmp()
        inout.FileOutput(input_file).write(self.sequence)
        output_file = get_file('GLIMMER_OUTPUT', None)
        if output_file is None:
            output_file = create_tmp()
        exit_code = subprocess.call([get_file('GLIMMER_PATH'), input_file, self.icm_file, output_file] + self.extra)
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
        with open(glimmer_output + '.detail') as f:
            glimmer_details = f.read()
        with open(glimmer_output + '.predict') as f:
            glimmer_predict = f.read()
        genes = list(self.read_genes(glimmer_output + '.detail'))
        return {
            'genes': genes,
            'glimmer_details': glimmer_details,
            'glimmer_predict': glimmer_predict,
            'glimmer_exit_code': glimmer_exit_code,
        }

def run(*args, **kwargs):
    return Glimmer(*args, **kwargs).run()