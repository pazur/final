import pylab

import Bio.Phylo

from settings import get_file

COMPULSORY_SETTINGS = ('TREE_IMAGE',)
ARGUMENTS = (
    'tree',
)

RESULTS = (
)
class Tree(object):
    def __init__(self, tree=None, *args, **kwargs):
        super(Tree, self).__init__(*args, **kwargs)
        self.tree = tree

    def run(self):
        Bio.Phylo.draw_graphviz(self.tree)
        pylab.savefig(get_file('TREE_IMAGE'))
        return {}


def run(*args, **kwargs):
    return Tree(*args, **kwargs).run()