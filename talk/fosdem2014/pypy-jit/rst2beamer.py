#!/usr/bin/env python
# encoding: utf-8
"""
A docutils script converting restructured text into Beamer-flavoured LaTeX.

Beamer is a LaTeX document class for presentations. Via this script, ReST can
be used to prepare slides. It can be called::

        rst2beamer.py infile.txt > outfile.tex

where ``infile.tex`` contains the produced Beamer LaTeX.

See <http:www.agapow.net/programming/python/rst2beamer> for more details.

"""
# TODO: modifications for handout sections?
# TOOD: sections and subsections?
# TODO: enable beamer themes?
# TODO: convert document metadata to front page fields?
# TODO: toc-conversion?
# TODO: fix descriptions

# Unless otherwise stated, created by P-M Agapow on 2007-08-21
# and open for academic & non-commercial use and modification .

__docformat__ = 'restructuredtext en'
__author__ = "Paul-Michael Agapow <agapow@bbsrc.ac.uk>"
__version__ = "0.2"


### IMPORTS ###

import locale
from docutils.core import publish_cmdline, default_description
from docutils.writers.latex2e import Writer as Latex2eWriter
from docutils.writers.latex2e import LaTeXTranslator, DocumentClass
from docutils import nodes

## Syntax highlighting:

"""
        .. sourcecode:: python

            My code goes here.


    :copyright: 2007 by Georg Brandl.
    :license: BSD, see LICENSE for more details.
"""

from pygments.formatters import HtmlFormatter, LatexFormatter

# The default formatter
DEFAULT = LatexFormatter()


from docutils.parsers.rst import directives

from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer

VARIANTS = {
    'linenos': LatexFormatter(linenos=True),
}

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # no lexer found - use the text one instead of an exception
        lexer = TextLexer()
    formatter = DEFAULT
    parsed = highlight(u'\n'.join(content), lexer, formatter)
    return [nodes.raw('', parsed, format='latex')]

pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
pygments_directive.options = dict([(key, directives.flag) for key in VARIANTS])

directives.register_directive('sourcecode', pygments_directive)


## multiple images as a single animation

"""
        .. animage:: foo-p*.pdf
           :align: center
           :scale: 50%
"""

from glob import glob
import copy
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image
import docutils

class Animage(Image): # Animated Image :-)
    
    def run(self):
        def raw(text):
            return docutils.nodes.raw('', text, format='latex')
        
        nodes = Image.run(self)
        img = nodes[0]
        if not isinstance(img, docutils.nodes.image):
            return nodes # not an image, WTF?
        newnodes = []
        pattern = img.attributes['uri']
        filenames = sorted(glob(pattern))
        for i, filename in enumerate(filenames):
            newimg = copy.deepcopy(img)
            newimg.attributes['uri'] = filename
            newnodes += [raw(r'\only<%d>{' % (i+1)),
                         newimg,
                         raw('}')]
        return newnodes

directives.register_directive('animage', Animage)




## CONSTANTS & DEFINES: ###

BEAMER_SPEC =   (
        'Beamer options',
        'These are derived almost entirely from the LaTeX2e options',
        tuple (
                [
                        (
                                'Specify theme.',
                                ['--theme'],
                                {'default': '', }
                        ),
                        (
                                'Specify document options.       Multiple options can be given, '
                                'separated by commas.  Default is "10pt,a4paper".',
                                ['--documentoptions'],
                                {'default': '', }
                        ),
                ] + list (Latex2eWriter.settings_spec[2][2:])
        ),
)

BEAMER_DEFAULTS = {
        'output_encoding': 'latin-1',
        'documentclass': 'beamer',
}


### IMPLEMENTATION ###

try:
         locale.setlocale (locale.LC_ALL, '')
except:
         pass

class BeamerTranslator (LaTeXTranslator):
        """
        A converter for docutils elements to beamer-flavoured latex.
        """

        def __init__ (self, document):
                LaTeXTranslator.__init__ (self, document)
                self.head_prefix = [x for x in self.head_prefix if ('{typearea}' not in x)]
                hyperref_posn = [i for i in range (len (self.head_prefix)) if ('{hyperref}' in self.head_prefix[i])]
                if not hyperref_posn:
                        self.head_prefix.append(None)
                        hyperref_posn = [-1] # XXX hack
                self.head_prefix[hyperref_posn[0]] = ('\\usepackage{hyperref}\n' +
                                                      '\\usepackage{fancyvrb}\n' +
                                                      LatexFormatter(style="manni").get_style_defs() +
                                                      "\n")

                self.head_prefix.extend ([
                        '\\definecolor{rrblitbackground}{rgb}{0.55, 0.3, 0.1}\n',
                        '\\newenvironment{rtbliteral}{\n',
                        '\\begin{ttfamily}\n',
                        '\\color{rrblitbackground}\n',
                        '}{\n',
                        '\\end{ttfamily}\n',
                        '}\n',
                ])
                # this fixes the hardcoded section titles in docutils 0.4
                self.d_class = DocumentClass ('article')

        def begin_frametag (self, node):
                if "verbatim" in str(node).lower():
                    return '\\begin{frame}[containsverbatim,fragile]\n'
                else:
                    return '\\begin{frame}\n'

        def end_frametag (self):
                return '\\end{frame}\n'

        def visit_section (self, node):
                if (self.section_level == 0):
                        self.body.append (self.begin_frametag(node))
                LaTeXTranslator.visit_section (self, node)

        def depart_section (self, node):
                # Remove counter for potential subsections:
                LaTeXTranslator.depart_section (self, node)
                if (self.section_level == 0):
                        self.body.append (self.end_frametag())

        def visit_title (self, node):
                if (self.section_level == 1):
                        self.body.append ('\\frametitle{%s}\n\n' % self.encode(node.astext()))
                        raise nodes.SkipNode
                else:
                        LaTeXTranslator.visit_title (self, node)

        def depart_title (self, node):
                if (self.section_level != 1):
                        LaTeXTranslator.depart_title (self, node)

        def visit_literal_block(self, node):
                 if not self.active_table.is_open():
                          self.body.append('\n\n\\smallskip\n\\begin{rtbliteral}\n')
                          self.context.append('\\end{rtbliteral}\n\\smallskip\n\n')
                 else:
                          self.body.append('\n')
                          self.context.append('\n')
                 if (self.settings.use_verbatim_when_possible and (len(node) == 1)
                                 # in case of a parsed-literal containing just a "**bold**" word:
                                 and isinstance(node[0], nodes.Text)):
                          self.verbatim = 1
                          self.body.append('\\begin{verbatim}\n')
                 else:
                          self.literal_block = 1
                          self.insert_none_breaking_blanks = 1

        def depart_literal_block(self, node):
                if self.verbatim:
                        self.body.append('\n\\end{verbatim}\n')
                        self.verbatim = 0
                else:
                        self.body.append('\n')
                        self.insert_none_breaking_blanks = 0
                        self.literal_block = 0
                self.body.append(self.context.pop())


class BeamerWriter (Latex2eWriter):
        """
        A docutils writer that modifies the translator and settings for beamer.
        """
        settings_spec = BEAMER_SPEC
        settings_defaults = BEAMER_DEFAULTS

        def __init__(self):
                Latex2eWriter.__init__(self)
                self.translator_class = BeamerTranslator




if __name__ == '__main__':
        description = (
                "Generates Beamer-flavoured LaTeX for PDF-based presentations." + default_description)
        publish_cmdline (writer=BeamerWriter(), description=description)


### END ######################################################################

