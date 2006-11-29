#!/usr/bin/env python
""" This is web server for slideshow which exports all the
necessary stuff for viewing pypy's presentation
"""

import py
from pypy.translator.js.examples import server

from pypy.rpython.ootypesystem.bltregistry import MethodDesc, BasicExternal,\
     described
from pypy.translator.js import commproxy
from pypy.translator.js.main import rpython2javascript

from pypy.translator.interactive import Translation

commproxy.USE_MOCHIKIT = True

FUNCTION_LIST = ['show', 'flow', 'annotate', 'rtype']

class ExportedMethods(BasicExternal):
    _render_xmlhttp = True

    def _create_t(self):
        if hasattr(self, 't'):
            return
        def f(x):
            return 1

        def g(x):
            return f(x) + 3

        self.t = Translation(g)

    @described(retval=None)
    def flow_basic(self):
        self._create_t()
        self.t.view()

    @described(retval=None)
    def annotate_basic(self):
        self._create_t()
        self.t.annotate([int])
        self.t.view()

    @described(retval=None)
    def rtype_basic(self):
        self._create_t()
        self.t.annotate([int])
        self.t.rtype()
        self.t.view()

exported_methods = ExportedMethods()
main_path = py.path.local(__file__).dirpath()

class Handler(server.TestHandler):
    exported_methods = exported_methods

    def index(self):
        return main_path.dirpath().join("fireworks-slides.html").open().read()
    index.exposed = True

    def jssource_js(self):
        import slideshow
        javascript_source = rpython2javascript(slideshow,
                FUNCTION_LIST)
        return "text/javascript", javascript_source
    jssource_js.exposed = True

    def MochiKit_js(self):
        return "text/javascript", main_path.join("MochiKit.js").open().read()
    MochiKit_js.exposed = True

    def style_css(self):
        return "text/css", main_path.dirpath().join("style.css").open().read()
    style_css.exposed = True

if __name__ == '__main__':
    server.start_server(handler=Handler, start_new=False)
