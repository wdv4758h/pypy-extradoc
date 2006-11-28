from py.__.documentation.confrest import *

class PyPyFireworksPage(Page): 
    def fill(self):
        super(PyPyFireworksPage, self).fill()
        self.body.attr.onload = 'show()'
        self.menubar[:] = []

class Project(Project):
    title = "PyPy Fireworks" 
    stylesheet = 'style.css'
    encoding = 'latin1' 
    prefix_title = "PyPy "
    logo = ''
    Page = PyPyFireworksPage

