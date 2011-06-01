NAME = 'settings'

MODULES = (
    'alignment',
    'tree',
)

PIPELINE = (
    #(module, {(source step, name): name}, {extra kwargs})
    ('alignment',
        {},
        {'only_tree': True}
    ), ('tree',
        {(0, 'tree'): 'tree'},
        {}
    ),
)

SUMMARY = (
    (0, 'tree_out'),
    (0, 'tree'),
)
SUMMARY_FILE = 'test/summary.txt'
SUMMARY_TYPE = 'HUMAN_READABLE'

### INOUT ###
INPUT_FORMAT = 'fasta'
INPUT_FILE = 'test/opuntia.fasta'

### ALIGNMENT ###
CLUSTALW_PATH = 'utilities/clustalw2'

# uncomment next lines to select clustalw output files instead of saving it to /tmp/
CLUSTALW_NEWTREE = 'test/newtree_file.dnd'
#CLUSTALW_OUTFILE = 'outfile.aln'

### TREE ###
TREE_IMAGE = 'test/tree.png'