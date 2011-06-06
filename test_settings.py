NAME = 'settings'

MODULES = (
    'alignment',
    'blast',
    'glimmer',
)

PIPELINE = (
    #(module, {(source step, name): name}, {extra kwargs}),
    ('glimmer',
        {},
        {},
    ),
    ('blast',
        {(0, 'genes'): 'sequence'},
        {}
    ),
    ('alignment',
        {(1, 'sequences'): 'sequences'},
        {},
    ),
)

SUMMARY = (
    (0, 'genes'),
    (1, 'sequences'),
    (2, 'alignment')
)
SUMMARY_FILE = 'summary.txt'
SUMMARY_TYPE = 'HUMAN_READABLE'

PREFIX = 'sequences' # prefiks dla wsyzstkich plikow z ustawien, ktore maja sciezke wzgledna

### INOUT ###
INPUT_FORMAT = 'fasta'
INPUT_FILE = 'seq1.fasta'

### ALIGNMENT ###
CLUSTALW_PATH = '/home/tomek/prog/bio/final/utilities/clustalw2'

# uncomment next lines to select clustalw output files instead of saving it to /tmp/
CLUSTALW_NEWTREE = 'newtree_file.dnd'
CLUSTALW_OUTFILE = 'outfile.aln'
#CLUSTALW_

### TREE ###
TREE_IMAGE = 'tree.png'

### GLIMMER ###
GLIMMER_PATH = '/home/tomek/prog/bio/final/utilities/glimmer3'
ICM_FILE = '/home/tomek/prog/bio/final/utilities/sample.icm'
GLIMMER_OUTPUT = 'glimmer_out'
