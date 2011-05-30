#! /usr/bin/python

import sys

import inout

if __name__ == '__main__':
    try:
        import settings
    except Exception as e:
        print e
        sys.exit(1)
    result = []
    for module in settings.modules:
        result = module.run(*result)
        result = [result]
