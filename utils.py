import tempfile

def create_tmp():
    file = tempfile.NamedTemporaryFile(delete=False)
    return file.name
