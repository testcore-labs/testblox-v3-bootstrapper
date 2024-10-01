import requests
import update
import client
import env
import sys
import log
import args
#import rpc
import colorama
import window

def main():
  window.w.mainloop()
  sys.exit()
  if args.args.place_id != None:
    # rpc.update_t(
    #   details="launching game...",
    #   start=rpc.start_time,
    #   large_image="https://cdn.discordapp.com/attachments/1128680651713957888/1289915198693707868/icon.png?ex=66fa8ea4&is=66f93d24&hm=c6c5fd34122b3d05319ced56867a464839bad3b83d5eeb455b59e9978fccc4a0&=&format=webp&quality=lossless",
    #   small_image="testblox-t",
    #   state=":3"
    # )
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