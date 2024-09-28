import env

def do(txt):
  print(txt)

def debug(txt):
  if env.app.debug:
    print(txt)