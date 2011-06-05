import tempfile

from summary import summary

def create_tmp():
    file = tempfile.NamedTemporaryFile(delete=False)
    return file.name