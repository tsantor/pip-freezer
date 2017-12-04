from __future__ import print_function

from codecs import open
from os import path

import pypandoc

here = path.abspath(path.dirname(__file__))

files = ['README.md', 'HISTORY.md']

for f in files:
    filepath = path.join(here, f)
    if path.exists(filepath):
        output_filename = path.splitext(f)[0]+'.rst'

        # Convert markdown to reStructured
        with open(filepath, encoding='utf-8') as f:
            content = pypandoc.convert(f.read(), 'rst', format='markdown')

        # Replace some RST underline chars that PyPI does not like
        # http://sphinx-doc.org/rest.html#sections
        content = content.replace('~', '^')

        # Write converted file
        with open(path.join(here, output_filename), 'w', encoding='utf8') as outfile:
            outfile.write(content)
    else:
        print('"{}" does not exist. Skipping...'.format(f))
        continue
