NAME = 'settings'

MODULES = (
    'alignment',
    'tree',
    'inout',
    'blast',
)

PIPELINE = (
    #(module, {(source step, name): name}, {extra kwargs})
    ('inout',
        {},
        {'type': 'SINGLE_SEQUENCE'}
    ),
    ('blast',
        {(0, 'file_content'): 'sequence'},
        {}
    ),
    ('alignment',
        {(1, 'sequences'): 'sequences'},
        {'only_tree': True}
    ), ('tree',
        {(2, 'tree'): 'tree'},
        {}
    ),
)

SUMMARY = (
    (2, 'tree_out'),
    (2, 'tree'),
)
SUMMARY_FILE = 'test/summary.txt'
SUMMARY_TYPE = 'HUMAN_READABLE'

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
#ICM_fILE = 'some_file.icm'