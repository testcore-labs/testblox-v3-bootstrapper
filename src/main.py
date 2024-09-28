import requests
import update
import client
import env
import args

def main():
  # does an update if it finds a new version
  if not args.args.disable_auto_update:
    update.do()
    
  place_id = args.args.place_id
  if place_id:
    client.join_place(args.args.place_id)
  else:
    exit("nothing to do")

main()