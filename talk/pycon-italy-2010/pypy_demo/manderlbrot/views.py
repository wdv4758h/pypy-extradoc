# Create your views here.

from django.http import HttpResponse

# only for benchmarking purposes
def empty(request):
    return HttpResponse('')

# render a manderlbrot image
def render(request):
    w = int(request.GET.get('w', 320))
    h = int(request.GET.get('h', 240))

    from py_mandel import manderlbrot
    img = manderlbrot(w, h)
    return HttpResponse(img, content_type="image/bmp")


# render a manderlbrot image through the execnet pypy child, which is set up
# below
def pypy_render(request):
    w = int(request.GET.get('w', 320))
    h = int(request.GET.get('h', 240))

    channel = pypy.remote_exec("""
        from py_mandel import manderlbrot
        w, h = channel.receive()
        img = manderlbrot(w, h)
        channel.send(img)
    """)
    channel.send((w, h))
    img = channel.receive()
    return HttpResponse(img, content_type="image/bmp")
    

# setup execnet and pypy child
#
# The setup is done here so that a single pypy-c is started and reused for all
# requests.  sys.path and cwd are set up so that py_mandel can be imported
# from remote_exec

import execnet
mygroup = execnet.Group()
pypy = mygroup.makegateway("popen//python=pypy-c")
pypy.remote_exec("""
    import sys
    import os
    os.chdir("manderlbrot")
    sys.path.insert(0, '')
""")


