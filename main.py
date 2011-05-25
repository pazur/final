import sys

settings = None


class ArgumentParser(object):
    def parse(self):
        settings_file = sys.argv[1]
        globals()['settings'] = __import__(settings_file)

if __name__ == '__main__':
    ArgumentsParser().parse()