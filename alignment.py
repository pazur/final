class Alignment(object):
    def run(self):
        return "Alignment"


def run(*args, **kwargs):
    return Alignment(*args, **kwargs).run()