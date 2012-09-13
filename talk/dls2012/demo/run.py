from io import mplayer, view
from analytics import Tracker
import sys

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = 'demo.avi'

tracker = Tracker()
while True:
    for img in mplayer(fn):
        view(img, 'Input')
        tracker.update(img)


