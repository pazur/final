from cStringIO import StringIO

import Bio.Phylo
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def summary(results):
    from settings import get_file
    from settings import get_setting
    data = get_setting('SUMMARY')
    file_path = get_file('SUMMARY_FILE')
    pipeline = get_setting('PIPELINE')
    with open(file_path,'w') as f:
        for number, key in data:
            f.write('\n==== step %d - %s (module %s)  ====\n' % (number, key, pipeline[number][0]))
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
    if isinstance(value, list):
        return ("[%d elements:\n" % len(value)) + "\n".join("\t" + human_readable(x) for x in value) + "\n]"
    if isinstance(value, SeqRecord):
        return "SEQ %s -- %s" % (value.id, value.description)
    if isinstance(value, Seq):
        return "SEQ of length %d: %s ... %s" % (len(value), Seq[:10], Seq[10:])
    return str(value)