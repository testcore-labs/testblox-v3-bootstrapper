import env
import config
import executable
import log

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

def check_if_invalid_api(res):
  return (res.status_code == 404)
  
def handle_invalid_api(res):
  if check_if_invalid_api(res):
    raise ConnectionError(f"api not implemented ({res.status_code})")

def check_if_down(res):
  return (res.status_code == 502)

def handle_is_down(res):
  if check_if_down(res):
    raise ConnectionError(f"server is down ({res.status_code})") 

def get(url):
  try:
    return None, requests.get(url)
  except error:
    if error is requests.exceptions.Timeout:
      raise ConnectionError("server is offline")

    return error, None

def game_info(game_id):
  err, res = get(f"{baseurl}/api/v1/game/info?id={game_id}")
  if err:
    print(err)
  handle_invalid_api(res)
  handle_is_down(res)
  if res.json()["message"] == "errors.type.not_a_place":
    log.warn("not a place, failed fetching place data")
  return res.json()

def get_latest_version(client_type):
  err, res = get(f"{baseurl}/api/v1/client/latest-version?type={client_type}")
  if err:
    print(err)
  handle_invalid_api(res)
  handle_is_down(res)
  try:
    return res.json()["info"]["version"]
  except:
    raise ConnectionError("expected JSON, got something else.")