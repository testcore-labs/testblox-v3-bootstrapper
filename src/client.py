import executable
import log
import env
import dsc
import window
import fetch
import config

import platform
import subprocess
import time
import os
import sys
import shutil

# of course you can spoof it but there's a check on the player itself
# that'll prevent you from running an older version
def get_version(client_type = "player"):
  return config.memory.get("clients", client_type, "version")

client_folder = os.path.join(executable.path, "clients")

def get_client_path(client_type = "player"):
  match client_type:
    case "player":
      return os.path.join(executable.path, "clients", f"{get_version("player")}", "player.exe")
    case "studio": 
      return os.path.join(executable.path, "clients", f"{get_version("studio")}", "studio.exe")

def is_client_installed(client_type):
  return os.path.exists(get_client_path(client_type))
def is_installed():
  return os.path.exists(client_folder) and is_client_installed("player") #and is_client_installed("studio")

def get_custom_env():
  # we use a custom prefix just so we don't fuck up things
  wine_prefix = executable.args.wine_prefix or f"/home/{os.getlogin()}/.tstblx/"
  custom_env = os.environ.copy()
  custom_env["WINEPREFIX"] = wine_prefix
  return custom_env

def get_executable(client_type = "player"):
  # since this will sit top-level of the client directory,
  # we can just use the current directory directly
  client_path = get_client_path(client_type)
  if not is_client_installed(client_type):
    log.throw(f"{client_path} does not exist.")
  else:
    return client_path

def run(custom_args = []): 
  client_path = get_executable("player")
  process = subprocess.call([
    f"{client_path}",
    *custom_args
  ],
  #env=get_custom_env(), 
  stdout=subprocess.DEVNULL,
  stderr=subprocess.STDOUT
  )

def run_wine(custom_args = []): 
  wine_path = executable.args.wine_path or "/usr/bin/wine"
  winetricks_path = executable.args.winetricks_path or "/usr/bin/winetricks"

  if not os.path.isfile(wine_path):
    log.throw("wine installation does not exist")

  if not os.path.isfile(winetricks_path):
    log.throw("winetricks installation does not exist")

  process_args = {
    'env': get_custom_env(), 
    'stdout': subprocess.DEVNULL,
    'stderr': subprocess.STDOUT
  }
  if config.bootstrapper.get("debug") or executable.args.debug:
    del process_args['stdout']

  wine_depends = [
    "d3dx9_43",
    "vcrun2005",
    "corefonts",
    "dotnet48"
  ]; 
  install_depends = executable.args.install_dependencies
  if install_depends:
    log.debug(f"got install dependencies: [{", ".join(install_depends)}]")
    install_depends = install_depends.split()
    wine_depends.extend(install_depends)

  # safety
  if executable.args.reinstall_wineprefix and os.path.isdir(process_args["env"]["WINEPREFIX"]):
    log.warn(f"DELETING wineprefix `{process_args["env"]["WINEPREFIX"]}` in 3 seconds")
    time.sleep(3)
    log.info(f"deleting...")
    shutil.rmtree(process_args["env"]["WINEPREFIX"])
  
  if not os.path.isdir(process_args["env"]["WINEPREFIX"]):
    log.info(f"installing dependencies: [{", ".join(wine_depends)}]")
    winetricks_process = subprocess.call([
    f"{winetricks_path}",
    "-q",
    *wine_depends
    ], env=get_custom_env())
    
  client_path = get_executable("player")
  wine_process = subprocess.call([
    f"{wine_path}",
    f"{client_path}",
    *custom_args
  ],
  **process_args
  )

def handle(): #[os_supported, os_name]
  os_name = platform.system()
  match os_name:
    case "Linux":
      os_distro = platform.freedesktop_os_release()
      # since we are going to use wine, we need to
      # install the neccesary packages to run
      # ROBLOX on wine.
      match os_distro:
        case "debian":
          # apt-get install
          # winbind
          return [True, os_name, os_distro]
        case _:
          return [False, os_name, os_distro]
    case "Darwin": 
      # might have to do the same with Linux.
      return [True, os_name, None]
    case "Windows":
      # run normally as we don't need a compatibility layer.
      return [True, os_name, None]
    case _:
      # return False as we don't know/support the OS.
      return [False, os_name, None]

def join_place(place_id):
  os_supported, os_name, os_distro = handle() 
  if os_supported:
    log.debug(f"detected os: {os_name}")

  dsc.update_playing(place_id)  
  game_info = fetch.game_info(place_id)
  if not game_info["success"]:
    log.throw("can't join game due to unsuccessful place request")
    return

  window.a.page("main").progress_text.configure(text=f"joining {game_info["info"]["title"]}")
  
  authenticationticket = executable.args.user_token
  authenticationurl = f"{fetch.baseurl}/Login/Negotiate.ashx"
  joinscripturl = f"{fetch.baseurl}/Game/PlaceLauncher.ashx?placeId={place_id}&request=RequestGame&isTeleport=true"
  time.sleep(0.2) # just for looks
  window.a.withdraw()
  # actually, we'll need you :)
  match os_name:
    case "Linux":
      # run under Wine, report an error if Wine isn't
      # installed or doesn't exist under 
      # /usr/bin/wine or --wine-path.)
      log.info("launching with wine")
      run_wine([
        "--authenticationTicket", authenticationticket,
        "--authenticationUrl", authenticationurl,
        "--joinScriptUrl", joinscripturl
      ])
    case "Windows":
      log.info("launching natively")
      run_native([
        "--authenticationTicket", authenticationticket,
        "--authenticationUrl", authenticationurl,
        "--joinScriptUrl", joinscripturl
      ])
    case _: 
      window.a.page("main").progress_text.configure(text="unsupported os")
      log.throw("unsupported os!")