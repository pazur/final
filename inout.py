import Bio.SeqIO

from settings import settings

class InputOutput(object):
    def __init__(self, format=None, *args, **kwargs):
        super(InputOutput, self).__init__(*args, **kwargs)
        if format is None:
            format = settings.INPUT_FORMAT
        self.format = format


class FileInputOutput(InputOutput):
    def __init__(self, file=None, *args, **kwargs):
        super(FileInputOutput, self).__init__(*args, **kwargs)
        if file is None:
            file = getatter(settings, self.default_file)
        self.file = file


class FileInput(FileInputOutput):
    default_file = 'INPUT_FILE'

    def read(self):
        return Bio.SeqIO.read(self.file, self.format)


class FileOutput(FileInputOutput):
    default_file = 'OUTPUT_FILE'

    def write(self, seq):
        return Bio.SeqIO.write(seq, self.file, self.format)
