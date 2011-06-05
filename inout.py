from cStringIO import StringIO
import Bio.SeqIO
import Bio.AlignIO

ARGUMENTS = (
    'file',     # input file path
    'format',   # input file format
    'type',     # input file type ('SINGLE_SEQUENCE', 'MULTIPLE_SEQUENCE', 'ALIGNMENT')
)

RESULTS = (
    'file_content',
)

class InputOutput(object):
    def __init__(self, format=None, *args, **kwargs):
        super(InputOutput, self).__init__(*args, **kwargs)
        if format is None:
            from settings import settings
            format = settings.INPUT_FORMAT
        self.format = format


class FileInputOutput(InputOutput):
    default_file = ""

    def __init__(self, file=None, *args, **kwargs):
        super(FileInputOutput, self).__init__(*args, **kwargs)
        if file is None:
            from settings import get_file
            file = get_file(self.default_file)
        self.file = file


class SingleSequenceFileInput(FileInputOutput):
    default_file = 'INPUT_FILE'

    def read(self):
        return Bio.SeqIO.read(self.file, self.format)


class MultipleSequenceFileInput(FileInputOutput):
    default_file = 'INPUT_FILE'

    def read(self):
        return list(Bio.SeqIO.parse(self.file, self.format))

class FileOutput(FileInputOutput):
    default_file = 'OUTPUT_FILE'

    def write(self, seq):
        return Bio.SeqIO.write(seq, self.file, self.format)

class AlignFileInput(FileInputOutput):
    default_file = 'ALIGN_FILE'

    def read(self):
        return Bio.AlignIO.read(self.file, format=self.format)

class StringOutput(InputOutput):
    def write(self, seq):
        s = StringIO()
        try:
            Bio.SeqIO.write(seq, s, self.format)
            return s.getvalue()
        finally:
            s.close()

def run(type, *args, **kwargs):
    if type == 'SINGLE_SEQUENCE':
        output = SingleSequenceFileInput(*args, **kwargs).read()
    elif type == 'MULTIPLE_SEQUENCE':
        output = MultipleSequenceFileInput(*args, **kwargs).read()
    elif type == 'ALIGNMENT':
        output = AlignFileInput(*args, **kwargs)
    else:
        raise Exception('Unknown input type')
    return {'file_content': output}
