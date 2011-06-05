from Bio.Blast import NCBIWWW,NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import inout
from settings import get_file

ARGUMENTS = (
    'program',      # Blast program - default blastn
    'database',     # Blast database - default nr
    'queryextra',   # Blast extra arguments
    'sequence',     # sequence to blast
)

RESULTS = (
    'blast_records', # blast result
    'sequences',    # sequences from result
)

class BlastSearch(object):
    def __init__(self, sequence=None, program="blastn", database="nr", queryextra={}, *args, **kwargs):
        super(BlastSearch, self).__init__(*args, **kwargs)
        if sequence is None:
            with open (get_file('INPUT_FILE')) as f:
                sequence = f.read()
        if isinstance(sequence, SeqRecord):
            sequence = sequence.seq
        if not isinstance(sequence, (Seq, basestring)):
            sequence = inout.StringOutput().write(sequence)
        self.sequence = sequence
        self.program = program
        self.database = database
        self.queryextra = queryextra

    def run(self):
        res = NCBIWWW.qblast(self.program, self.database, self.sequence, **self.queryextra)
        blast_records = NCBIXML.parse(res)
        alignments = reduce(lambda x, y: x + y, map(lambda r: r.alignments, blast_records), [])
        records = list(self.get_seqrecords(alignments))
        records = self.delete_same(records)
        return {
            'blast_xml': res.getvalue(),
            'blast_records': blast_records,
            'sequences': records,
        }

    def delete_same(self, records):
        result = []
        result_ids = []
        for record in records:
            if record.id not in result_ids :
                result.append(record)
                result_ids.append(record.id)
        return result

    def get_seqrecords(self, alignments):
        for alignment in alignments:
            for hsp in alignment.hsps:
                yield SeqRecord(Seq(hsp.sbjct), id=alignment.hit_id, description=alignment.hit_def)


def run(*args, **kwargs):
    return BlastSearch(*args, **kwargs).run()