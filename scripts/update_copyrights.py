#!/usr/bin/env python

import os
import re
import sys


COPYRIGHT_RE = re.compile('# Copyright \\(C\\).*?\\n')
COPYRIGHT = '# Copyright (C) 2012, 2013 richard contributors.  See AUTHORS.


def copyright_py(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()

    if COPYRIGHT_RE.search(data) != None:
        data = COPYRIGHT_RE.sub(COPYRIGHT, data)
        f = open(filename, 'w')
        f.write(data)
        f.close()


def main(argv):
    if '--doit' not in argv:
        print 'Usage: {0} --doit'.format(__file__)
        print 'Updates the copyright on all Python files.'
        return 1

    top_level = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir))

    print 'Starting at {0}'.format(top_level)

    for root, dirs, files in os.walk(top_level):
        for name in files:
            # Don't update this file!
            if name == __file__:
                continue

            if name.endswith('.py'):
                filename = os.path.join(root, name)
                print 'Fixing {0}'.format(filename)
                copyright_py(filename)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
