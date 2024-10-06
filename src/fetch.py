import env
import config
import executable

import requests

baseurl = executable.args.baseurl or config.bootstrapper.get("baseurl")

# should return (EXAMPLE)
# { success: true, message: "", {
#   id: 1818,
#   thumbnail: "https://tr.rbxcdn.com", # must be a publicly-accesible URL, preferably PNG
#   title: "Crossroads",
#   description: "Something interesting and neat about this specific game",
#   year: 2019, # OPTIONAL
#   players: 0,
#   max_players: 25
# } }
#
# if it fails                cant guarantee that you'll get this exact res.json()["messsage"] 
# { success: false, message: "why.it.failed.here.noob" }

def game_info(game_id):
  res = requests.get(f"{baseurl}/api/v1/game/info?id={game_id}")
  return res.json()

def get_latest_version(client_type):
  res = requests.get(f"{baseurl}/api/v1/client/latest-version?type={client_type}")
  try:
    return res.json()["info"]["version"]
  except:
    raise ConnectionError("expected JSON, got something else.")