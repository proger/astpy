"""
Goal:
    inject a docstring into a function from a dictionary
"""

import sys
import ast
from walker import Walker

namemap = {}        # override this in ipython


class WalkerCallback(object):
    def __init__(self):
        self.injections = {}

    def __call__(self, walker, node):
        if node.__class__.__name__ != 'FunctionDef':
            return

        args = getattr(getattr(node, 'args', None), 'args', [])
        line = max([node.lineno] + [a.lineno for a in args])

        if node.name in namemap:
            self.injections[line] = (walker.level, namemap[node.name])


def main(filename):
    with open(filename) as f:
        source = f.readlines()

    root = ast.parse(filename=filename, source=''.join(source))
    wcb = WalkerCallback()
    ast.walk(root, Walker(stream=None, callback=wcb))

    def write():
        for lineno, line in enumerate(source, 1):
            yield line
            if lineno in wcb.injections:
                level, s = wcb.injections[lineno]
                yield '%s"%s"\n' % (level * '    ', s)

    return ''.join(write())
