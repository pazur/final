from cStringIO import StringIO

import Bio.Phylo

def summary(results):
    from settings import get_setting
    data = get_setting('SUMMARY')
    file_path = get_setting('SUMMARY_FILE')
    pipeline = get_setting('PIPELINE')
    with open(file_path,'w') as f:
        for number, key in data:
            f.write('==== step %d - %s (module %s)  ====\n' % (number, key, pipeline[number][0]))
            f.write(format(results[number][key]))


def format(value):
    from settings import get_setting
    summary_type = get_setting('SUMMARY_TYPE')
    if summary_type == "HUMAN_READABLE":
        return human_readable(value)
    else:
        return str(value)

def human_readable(value):
    if isinstance(value, Bio.Phylo.Newick.Tree):
        f = StringIO()
        Bio.Phylo.draw_ascii(value, file=f)
        result = f.getvalue()
        f.close()
        return result
    return str(value)