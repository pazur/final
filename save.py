import inout
from utils import create_tmp

class Save(object):
    def __init__(self, to_save, file_path=None, *args, **kwargs):
        if file_path is None:
            file_path = create_tmp()
        self.file_path = file_path

    def run(self):
        return {'file': self.file_path}

def run(*args, **kwargs):
    return Save(*args, **kwargs).run()