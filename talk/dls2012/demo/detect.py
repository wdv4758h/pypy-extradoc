from reloader import autoreload
from io import view, viewsc

def morph(fg, r, fn):
    res = fg.new()
    for y in xrange(fg.height):
        for x in xrange(fg.width):
            #res[x, y] = max(fg[x+dx, y+dy] 
            #                for dx in xrange(-r, r+1) 
            #                for dy in xrange(-r, r+1))
            res[x, y] = fg[x, y]
            for dx in xrange(-r, r+1):
                for dy in xrange(-r, r+1):
                    res[x, y] = fn(res[x, y], fg[x+dx, y+dy])
    return res

def morph(fg, r, fn):
    xres = fg.new()
    for y in xrange(fg.height):
        for x in xrange(fg.width):
            xres[x, y] = fg[x, y]
            for dx in xrange(-r, r+1):
                xres[x, y] = fn(xres[x, y], fg[x+dx, y])
    res = fg.new()
    for y in xrange(fg.height):
        for x in xrange(fg.width):
            res[x, y] = xres[x, y]
            for dy in xrange(-r, r+1):
                res[x, y] = fn(res[x, y], xres[x, y+dy])
    return res

def erode(fg, r=1):
    return morph(fg, r, min)

def dilate(fg, r=1):
    return morph(fg, r, max)

class Labler(object):
    def __init__(self, seg):
        self.labels = seg.new()
        self.last_label = 0
        self.done = False

    def update(self, x, y, neighbours):
        neighbours = set(neighbours)
        neighbours.discard(0)
        if not neighbours:
            self.last_label += 1
            l = self.last_label
        else:
            l = min(neighbours)
        if self.labels[x, y] != l:
            self.done = False
        self.labels[x, y] = l

    def __getitem__(self, (x, y)):
        return self.labels[x, y]


def bwlabel(seg):
    labels = Labler(seg)
    while not labels.done:
        labels.done = True
        for y in xrange(seg.height):
            for x in xrange(seg.width):
                if seg[x, y]:
                    ll = [labels[x, y], labels[x-1, y], labels[x-1, y-1], labels[x, y-1], labels[x+1, y-1]]
                    labels.update(x, y, ll)

        for y in reversed(xrange(seg.height)):
            for x in reversed(xrange(seg.width)):
                if seg[x, y]:
                    ll = [labels[x, y], labels[x+1, y], labels[x-1, y+1], labels[x, y+1], labels[x+1, y+1]]
                    labels.update(x, y, ll)

    return labels.labels

class BoundingBox(object):
    maxx = maxy = float('-Inf')
    minx = miny = float('Inf')

    def add(self, x, y):
        self.maxx = max(self.maxx, x)
        self.maxy = max(self.maxy, y)
        self.minx = min(self.minx, x)
        self.miny = min(self.miny, y)

    def draw(self, img):
        for y in xrange(self.miny, self.maxy + 1):
            img[self.maxx, y] = 255
            img[self.minx, y] = 255
        for x in xrange(self.minx, self.maxx + 1):
            img[x, self.miny] = 255
            img[x, self.maxy] = 255

    def area(self):
        return (self.maxx - self.minx + 1) * (self.maxy - self.miny + 1)

def extract_boxes(labels):
    boxes = {}
    for y in xrange(labels.height):
        for x in xrange(labels.width):
            l = labels[x, y]
            if l:
                if l not in boxes:
                    boxes[l] = BoundingBox()
                boxes[l].add(x, y)
    return boxes.values()


@autoreload
def find_objects(fg, minarea=100):
    seg = erode(dilate(fg, 3), 4)
    labels = bwlabel(seg)
    boxes = extract_boxes(labels)
    boxes = [b for b in boxes if b.area() >= minarea]
    view(64*labels, 'segments')
    return boxes
