#! /usr/bin/python

import sys

if __name__ == '__main__':
    try:
        import settings
    except Exception as e:
        print e
        sys.exit(1)
    result = {}
    for module in settings.settings.PIPELINE:
        result = settings.modules[module].run(**result)
    print result
