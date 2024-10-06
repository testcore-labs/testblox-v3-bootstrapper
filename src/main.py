import update
import client
import env
import log
import window
import dsc
import executable
import fetch
import uri_scheme
import installer

import time
import requests
import sys

log.debug(f"args: {sys.argv}")
log.debug(f"baseurl: {fetch.baseurl}")
log.debug(f"path: {executable.path}")
log.debug(f"exe: {executable.exe}")
def main():
  dsc.update_loading()
  if executable.args.place_id != None:
    if not executable.args.ignore_not_installed and not installer.installed():
      installer.install()

    # does an update if it finds a new version
    if not executable.args.disable_auto_update:
      update.do()
      
    place_id = executable.args.place_id
    if place_id:
      client.join_place(executable.args.place_id)
  else:
    # the first argument is the path to the script/executable
    if len(sys.argv) == 1:
      executable.parser.print_help(sys.stderr)
      sys.exit(0) 

main()