import requests
import update
import client
import env
import sys
import args

def main():
  # checks if `clients` dir exists on the same path as the executable
  if not args.args.ignore_not_installed and not client.is_installed():
    print("not installed")
    sys.exit(1) 

  # does an update if it finds a new version
  if not args.args.disable_auto_update:
    update.do()
    
  place_id = args.args.place_id
  if place_id:
    client.join_place(args.args.place_id)
  else:
    print("nothing to do")
    sys.exit(0) 

main()