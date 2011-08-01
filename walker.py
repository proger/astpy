import sys
from ast import walk, get_child_nodes

class Walker(object):
    def __init__(self, level=0, stream=sys.stdout, callback=None):
        self.level = level
        self.stream = stream
        self.callback = callback

    def generic(self, node):
        name = getattr(node, 'name', '')
        line = getattr(node, 'lineno', '')
        col = getattr(node, 'col_offset', '')

        suffix = ':%s:%s' % (line, col) if line or col else ''

        if self.stream:
            self.stream.write('{indent}{type}{name} {data}\n'.format(
                indent='  ' * self.level, type=node.__class__.__name__,
                data={k:v for k,v in node.__dict__.items() if k not in (
                        'body', 'name', 'args'
                    ) if v},
                name=(' "%s" %s' % (name, suffix)) if name else ''
            ))

        if callable(self.callback):
            self.callback.__call__(self, node)

        for child in get_child_nodes(node):
            walk(child, type(self)(
                self.level + 1,
                stream=self.stream,
                callback=self.callback))

    def __getattr__(self, name):
        return self.generic
