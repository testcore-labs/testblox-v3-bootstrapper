# wow
import sys, os
if getattr(sys, 'frozen', False):
    path = os.path.dirname(os.path.realpath(sys.executable))
else:
    path = os.path.dirname(os.path.realpath(__file__))
