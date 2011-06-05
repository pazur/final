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
SUMMARY_FILE = 'test/summary.txt'
SUMMARY_TYPE = 'HUMAN_READABLE'

PREFIX = ''

### INOUT ###
INPUT_FORMAT = 'fasta'
INPUT_FILE = 'test/single.fasta'

### ALIGNMENT ###
CLUSTALW_PATH = 'utilities/clustalw2'

# uncomment next lines to select clustalw output files instead of saving it to /tmp/
CLUSTALW_NEWTREE = 'test/newtree_file.dnd'
#CLUSTALW_OUTFILE = 'outfile.aln'
#CLUSTALW_

### TREE ###
TREE_IMAGE = 'test/tree.png'

### GLIMMER ###
GLIMMER_PATH = 'utilities/glimmer3'
ICM_FILE = 'test/sample.icm'
GLIMMER_OUTPUT = 'test/glimmer_out'