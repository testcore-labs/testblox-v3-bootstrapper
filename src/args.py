import argparse

parser = argparse.ArgumentParser(
  description = "a ROBLOX client bootstrapper."
)

parser.add_argument(
  '--wine-path', 
  type=str,
  help='sets the wine path | only for Linux/Darwin'
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
  '--disable-auto-update', 
  action='store_true',
  help='disables auto-update, this does not bypass client version/hash checking'
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

args = parser.parse_args()