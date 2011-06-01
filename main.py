#! /usr/bin/python

import sys

from summary import summary

if __name__ == '__main__':
    try:
        import settings
    except Exception as e:
        print e
        sys.exit(1)
    results = []
    #result = {}
    #for module in settings.settings.PIPELINE:
    #    result = settings.modules[module].run(**result)
    for number, (module_name, arguments, extra) in enumerate(settings.settings.PIPELINE):
        kwargs = {}
        for (source_number, old_arg), new_arg in arguments.iteritems():
            kwargs[new_arg] = results[source_number][old_arg]
        kwargs.update(extra)
        results.append(settings.modules[module_name].run(**kwargs))
    summary(results)
