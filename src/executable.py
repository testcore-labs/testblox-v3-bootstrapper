# wow
import sys, os

import argparse

xdg = False
uri = "tstblx-bootstrapper"
if len(sys.argv) >= 1:
  for i, arg in enumerate(sys.argv):
    if arg.startswith(uri):
      xdg = True
      arg = arg.replace(f"{uri}://", "")
      del sys.argv[i]
      sys.argv.extend(arg.split())
      
parser = argparse.ArgumentParser(
  description = "a ROBLOX client bootstrapper."
)

parser.add_argument(
  '--wine-path', 
  type=str,
  help='sets the wine path | only for Linux/Darwin'
)
parser.add_argument(
  '--winetricks-path', 
  type=str,
  help='sets the winetricks path | only for Linux/Darwin'
)
parser.add_argument(
  '--wine-prefix', 
  type=str,
  help='sets the wine prefix | only for Linux/Darwin'
)
parser.add_argument(
  '--baseurl', 
  type=str,
  help='only set this if you know what you are doing!'
)
parser.add_argument(
  '--debug', 
  action='store_true',
  help='debugger, shows useful information'
)
parser.add_argument(
  '--disable-auto-update', 
  action='store_true',
  help='disables auto-update, this does not bypass client version/hash checking'
)
parser.add_argument(
  '--ignore-not-installed', 
  action='store_true',
  help='testing purposes only'
)
parser.add_argument(
  '--custom-path', 
  type=str,
  help='dev only'
)

# the nitty gritty
parser.add_argument(
  '--place-id',
  type=int,
  help='joins a specific place'
)
parser.add_argument(
  '--user-token', 
  type=str,
  help='uses the user token given to join a place as that user'
)

args, unknown = parser.parse_known_args(sys.argv)

if getattr(sys, 'frozen', False):
  #pyinstaller
  pyinstaller = True
  unpacked = os.path.dirname(os.path.realpath(__file__))
  assets = os.path.join(unpacked, "assets")
  path = args.custom_path or os.path.dirname(os.path.realpath(sys.executable))
  exe = os.path.realpath(sys.executable)
else:
  #py
  pyinstaller = False
  unpacked = os.path.dirname(os.path.realpath(__file__))
  assets = os.path.join(".", "assets")
  path = args.custom_path or os.path.dirname(os.path.realpath(__file__))
  exe = os.path.realpath(__file__)
