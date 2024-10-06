import env

from plumbum import colors
import config
import sys
import time

formating = "[{time}] [{from_where}]: {text}"

def info(txt):
  formatted = formating.format(
    time=time.strftime("%Y-%m-%d %H:%M:%S") | colors.bold,
    from_where="INFO" | colors.bold,
    text=txt
  )
  print(formatted)

def warn(txt):
  formatted = formating.format(
    time=time.strftime("%Y-%m-%d %H:%M:%S") | colors.bold,
    from_where="WARN" | colors.yellow,
    text=txt
  )
  print(formatted)

def debug(txt):
  if config.bootstrapper.get("debug") or executable.args.debug:
    formatted = formating.format(
      time=time.strftime("%Y-%m-%d %H:%M:%S") | colors.bold,
      from_where="DEBUG" | colors.green,
      text=txt
    )
    print(formatted)

def throw(txt):
  formatted = formating.format(
    time=time.strftime("%Y-%m-%d %H:%M:%S") | colors.bold,
    from_where="ERROR" | colors.red,
    text=txt
  )
  print(formatted)
  sys.exit(1)

def exit(txt):
  formatted = formating.format(
    time=time.strftime("%Y-%m-%d %H:%M:%S") | colors.bold,
    from_where="EXIT" | colors.orange1,
    text=txt
  )
  print(formatted)
  sys.exit(0)