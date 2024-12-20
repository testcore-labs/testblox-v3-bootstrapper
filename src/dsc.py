import window
import config
import fetch
import env

import pypresence
import threading
import time
import log

RPC = pypresence.Presence(client_id=env.discord.client_id)

connection_thread = None
connection_successful = False
enabled_rpc = lambda : config.bootstrapper.get("discord", "rpc", "enabled")

def update_async(**kwargs):
  if not enabled_rpc():
    return
  global connection_thread
  def do_connect():
    global connection_successful
    try:
      log.debug("trying to connect RPC")
      rpc_connect = RPC.connect()
      connection_successful = True
      log.debug(f"RPC connect: {rpc_connect}")
    except Exception as error:
      connection_successful = False
      if isinstance(error, pypresence.exceptions.DiscordNotFound):
        log.warn("Discord is not launched, RPC ignored") 
      else:
        log.warn(f"unknown error occured, {error}")
  if connection_thread is None:
    connection_thread = threading.Thread(target=do_connect, daemon=True)
    connection_thread.start()
  
  connection_thread.join()
  if connection_successful:
    RPC.update(**kwargs)
  else:
    log.warn("RPC could not be set as connection was unsuccessful.")

def update_sync(**kwargs):
  if not enabled_rpc():
    return
  thread = threading.Thread(target=update_async, args=kwargs, daemon=True)
  thread.start()
  return thread

def update_loading():
  if not enabled_rpc():
    return
  update_async(
    large_image="testblox-t", large_text="loading",
    small_image="testblox-t", small_text="i said im loading",

    details="loading...",
    start=env.timings.start, state=f"wait patiently..",
  )

def update_playing(place_id):
  if not enabled_rpc():
    return
  game_info = fetch.game_info(place_id) # game/root_place
  if not game_info["success"]:
    log.warn("failed setting `playing` presence")
    return
  party_size = None
  if int(game_info["info"]["players"]) > 0 and int(game_info["info"]["max_players"]) > 0:
    party_size = [
      int(game_info["info"]["players"]),
      int(game_info["info"]["max_players"])
    ]
  update_async(
    large_image=(game_info["info"]["thumbnail"]), large_text="game icon",
    small_image="testblox-t", small_text=f"{game_info["info"]["year"]}",

    details=game_info["info"]["title"],
    start=env.timings.start, state=f"by {game_info["info"]["creator"]}", party_size=party_size,
  )