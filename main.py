#! /usr/bin/python

import sys

if __name__ == '__main__':
    try:
        import settings
    except Exception as e:
        print e
        sys.exit(1)
    print settings.settings