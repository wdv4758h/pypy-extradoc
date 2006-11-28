#!/usr/bin/env python
""" This is web server for slideshow which exports all the
necessary stuff for viewing pypy's presentation
"""

import py
from py.__.test.rsession import web

from pypy.rpython.ootypesystem.bltregistry import MethodDesc, BasicExternal,\
     described
from pypy.translator.js.main import rpython2javascript, Options
from pypy.translator.js import commproxy
from pypy.translator.js import json

from pypy.translator.interactive import Translation

commproxy.USE_MOCHIKIT = True

FUNCTION_LIST = ['show', 'flow']

class ExportedMethods(BasicExternal):
    _render_xmlhttp = True

    def _create_t(self):
        if hasattr(self, 't'):
            return
        def f(x):
            return 1

        def g(x):
            return f(x) + 3

        self.t = Translation(f)

    @described(retval=None)
    def flow_basic(self):
        self._create_t()
        self.t.view()
        return json.write(None)

exported_methods = ExportedMethods()
main_path = py.path.local(__file__).dirpath()

class Handler(web.TestHandler):
    exported_methods = exported_methods

    def run_(self):
        self.run_index()
    
    def run_index(self):
        data_name = main_path.dirpath().join("fireworks-slides.html")
        data = data_name.open().read()
        self.serve_data("text/html", data)

    def run_jssource_js(self):
        import slideshow
        javascript_source = rpython2javascript(slideshow,
                FUNCTION_LIST)
        self.serve_data("text/javascript", javascript_source)

    def run_MochiKit_js(self):
        self.serve_data("text/javascript", main_path.join("MochiKit.js").open().read())

if __name__ == '__main__':
    web.start_server(handler=Handler, start_new=False)
