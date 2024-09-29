import sys
import env

def do(txt):
  print(txt)

def debug(txt):
  if env.app.debug:
    print(txt)

def throw(txt):
  if env.app.debug:
    print(txt)
    sys.exit(1)

def exit(txt):
  if env.app.debug:
    print(txt)
    sys.exit(0)