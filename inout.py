import Bio.SeqIO
import Bio.AlignIO

class InputOutput(object):
    def __init__(self, format=None, *args, **kwargs):
        super(InputOutput, self).__init__(*args, **kwargs)
        if format is None:
            from settings import settings
            format = settings.INPUT_FORMAT
        self.format = format


class FileInputOutput(InputOutput):
    def __init__(self, file=None, *args, **kwargs):
        super(FileInputOutput, self).__init__(*args, **kwargs)
        if file is None:
            from settings import settings
            file = getattr(settings, self.default_file)
        self.file = file


class SingleSequenceFileInput(FileInputOutput):
    default_file = 'INPUT_FILE'

    def read(self):
        return Bio.SeqIO.read(self.file, self.format)


class MultipleSequenceFileInput(FileInputOutput):
    default_file = 'INPUT_FILE'

    def read(self):
        return Bio.SeqIO.parse(self.file, self.format)

class FileOutput(FileInputOutput):
    default_file = 'OUTPUT_FILE'

    def write(self, seq):
        return Bio.SeqIO.write(seq, self.file, self.format)

class AlignFileInput(FileInputOutput):
    default_file = 'ALIGN_FILE'

    def read(self):
        return Bio.AlignIO.read(self.file, format=self.format)