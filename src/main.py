import requests
import update
import client
import env
import sys
import log
import args

def main():
  if args.args.place_id != None:
    # checks if `clients` dir exists on the same path as the executable
    if not args.args.ignore_not_installed and not client.is_installed():
      log.throw("not installed")

    # does an update if it finds a new version
    if not args.args.disable_auto_update:
      update.do()
    
    place_id = args.args.place_id
    if place_id:
      client.join_place(args.args.place_id)
  else:
    # the first argument is the path to the script/executable
    if len(sys.argv) == 1:
      args.parser.print_help(sys.stderr)
      sys.exit(0) 

main()