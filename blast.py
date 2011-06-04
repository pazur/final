from Bio.Blast import NCBIWWW,NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

ARGUMENTS = (
    'program',      # Blast program - default blastn
    'database',     # Blast database - default nr
    'queryextra',   # Blast extra arguments
    'sequence',     # sequence to blast
)

RESULTS = (
    'blast_record', # blast result
    'sequences',    # sequences from result
)

class BlastSearch(object):
    def __init__(self, sequence, program="blastn", database="nr", queryextra={}, *args, **kwargs):
        super(BlastSearch, self).__init__(*args, **kwargs)
        self.sequence = sequence.seq
        self.program = program
        self.database = database
        self.queryextra = queryextra

    def run(self):
        res = NCBIWWW.qblast(self.program, self.database, self.sequence, **self.queryextra)
        blast_record = NCBIXML.read(res)
        records = list(self.get_seqrecords(blast_record.alignments))
        return {
            'blast_record': blast_record,
            'sequences': records,
        }

    def get_seqrecords(self, alignments):
        for alignment in alignments:
            for hsp in alignment.hsps:
                yield SeqRecord(Seq(hsp.sbjct), id=alignment.accession)


def run(*args, **kwargs):
    return BlastSearch(*args, **kwargs).run()