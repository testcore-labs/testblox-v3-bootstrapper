import platform
import log
import subprocess
import args
import executable
import os

client_types = {
  "studio": 0,
  "player": 1,
}
client_paths = {
  "clients": os.path.join(executable.path, "clients"),
  "player": os.path.join(executable.path, "clients", "player", "realclient.exe")
}

def is_installed():
  return os.path.exists(client_paths["clients"])

def get_version():
  return "version-faggotfag"

def get_executable():
  # since this will sit top-level of the client directory,
  # we can just use the current directory directly
  client_path = client_paths["player"]
  if os.path.isfile(client_path):
    return client_path
  else:
    raise ValueError(f"{client_path} does not exist.")

def run_wine(custom_args = []): 
  wine_path = args.args.wine_path or "/usr/bin/wine"
  # we use a custom prefix just so we don't fuck up things
  wine_prefix = args.args.wine_prefix or f"/home/{os.getlogin()}/.tstblx/"
  custom_env = os.environ.copy()
  custom_env["WINEPREFIX"] = wine_prefix
  command = subprocess.run([f"{wine_path}", get_executable(), *custom_args], env=custom_env)

def handle(): #[sucessful, os_supported, os_name]
  os_name = platform.system()
  match os_name:
    case "Linux":
      return [False, True, os_name]
    case "Darwin": 
      # might have to do the same with Linux.
      return [False, True, os_name]
    case "Windows":
      # run normally as we don't need a compatibility layer.
      return [False, True, os_name]
    case _:
      # return False as we don't know/support the OS.
      return [False, False, os_name]

def join_place(place_id):
  sucessful, os_supported, os_name = handle() 
  if os_supported:
    log.debug(f"detected os: {os_name}")
  
  # we have to fetch a joinscript in order to join

  match os_name:
    case "Linux":
      # run under Wine, report an error if Wine isn't
      # installed or doesn't exist under 
      # /usr/bin/wine or --wine-path.
      log.do("joining")
      run_wine([""])
    case _: 
      log.do("unsupported os!")