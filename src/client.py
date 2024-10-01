import platform
import log
import subprocess
import args
import executable
import os
import sys
import env

client_types = {
  "studio": 0,
  "player": 1,
}
client_paths = {
  "clients": os.path.join(executable.path, "clients"),
  "player": args.args.player_path or os.path.join(executable.path, "clients", "player", "RobloxPlayerBeta.exe"),
  "studio": os.path.join(executable.path, "clients", "studio", "robloxstudiobeta.exe")
}

def is_client_installed(client_type):
  return os.path.exists(client_paths[client_type])
def is_installed():
  return os.path.exists(client_paths["clients"]) and is_client_installed("player") #and is_client_installed("studio")

# of course you can spoof it but there's a check on the player itself
# that'll prevent you from running an older version
def get_version():
  return "version-faggotfag"

def get_custom_env():
  # we use a custom prefix just so we don't fuck up things
  wine_prefix = args.args.wine_prefix or f"/home/{os.getlogin()}/.tstblx/"
  custom_env = os.environ.copy()
  custom_env["WINEPREFIX"] = wine_prefix
  return custom_env

def get_executable(client_type = "player"):
  # since this will sit top-level of the client directory,
  # we can just use the current directory directly
  client_path = client_paths[client_type]
  if not is_client_installed(client_type):
    log.throw(f"{client_path} does not exist.")
  else:
    return client_path

def run_wine(custom_args = []): 
  wine_path = args.args.wine_path or "/usr/bin/wine"
  winetricks_path = args.args.winetricks_path or "/usr/bin/winetricks"

  if not os.path.isfile(wine_path):
    log.throw("wine installation does not exist")

  if not os.path.isfile(winetricks_path):
    log.throw("winetricks installation does not exist")

  if not True:
    winetricks_process = subprocess.call([
    f"{winetricks_path}",
    "-q",
    #"dxvk",
    "d3dx9_43",
    "vcrun2005",
    "corefonts",
    "dotnet48"
    ], env=get_custom_env())

  client_path = get_executable("player")
  wine_process = subprocess.call([
    f"{wine_path}",
    f"{client_path}",
    *custom_args
  ],
  env=get_custom_env(), 
  stdout=subprocess.DEVNULL,
  stderr=subprocess.STDOUT
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

  match os_name:
    case "Linux":
      # run under Wine, report an error if Wine isn't
      # installed or doesn't exist under 
      # /usr/bin/wine or --wine-path.
      authenticationticket = "ass"
      authenticationurl = f"{args.args.baseurl or env.app.baseurl}/Login/Negotiate.ashx"
      joinscripturl = f"{args.args.baseurl or env.app.baseurl}/Game/PlaceLauncher.ashx?placeId={place_id}&request=RequestGame&isTeleport=true"
      log.do("joining")
      run_wine([
        "--authenticationTicket", authenticationticket,
        "--authenticationUrl", authenticationurl,
        "--joinScriptUrl", joinscripturl
      ])
    case _: 
      log.throw("unsupported os!")