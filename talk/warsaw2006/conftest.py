
import py
import re
from py.__.documentation.conftest import Directory, DoctestText, ReSTChecker
from py.__.documentation.conftest import ReSTSyntaxTest

class SlideshowReSTSyntaxTest(ReSTSyntaxTest):
    def run(self):
        super(SlideshowReSTSyntaxTest, self).run()
        path = self.fspath
        # XXX dirty hack
        htmlpath = path.dirpath().join(path.basename[:-4] + ".html")
        data = htmlpath.open().read()
        htmlpath.open("w").write(re.sub("<body>", "<body onload='show()'>",
                                        data))

class SlideshowReSTChecker(ReSTChecker):
    ReSTSyntaxTest = SlideshowReSTSyntaxTest

#    def execute(self, *args, **kwargs):
#        super(SlideshowReSTChecker, self).execute(*args, **kwargs)
    
class Directory(Directory): 
    ReSTChecker = SlideshowReSTChecker
