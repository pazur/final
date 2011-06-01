NAME = 'settings'

MODULES = (
    'alignment',
)

PIPELINE = (
    'alignment',
)

### INOUT ###
INPUT_FORMAT = 'fasta'
INPUT_FILE = 'opuntia.fasta'

### ALIGNMENT ###
CLUSTALW_PATH = 'utilities/clustalw2'

# uncomment next lines to select clustalw output files instead of saving it to /tmp/
#CLUSTALW_NEWTREE = 'newtree_file.dnd'
#CLUSTALW_OUTFILE = 'outfile.aln'