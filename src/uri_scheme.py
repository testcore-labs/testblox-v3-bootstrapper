import env
import executable
import init

import platform
import shutil
import subprocess
import os
# cross platform uri scheme assigner
exe = executable.exe
bootstrapper_mime = f"""[Desktop Entry]
Type=Application
Name={env.app.name}
Exec={executable.exe} %u
StartupNotify=false
{"Terminal=true\nTerminalOptions=\\s--noclose" if init.debug else ""}
MimeType=x-scheme-handler/{executable.uri};
"""

xdg = os.path.join(executable.path, "mime")
bootstrapper_desktop = os.path.join(xdg, "testblox-bootstrapper.desktop")
os_name = platform.system()
def exists():
  return os.path.exists(xdg) and os.path.exists(bootstrapper_desktop)

def set_uri():
  match os_name:
    case "Linux":
      if not os.path.exists(xdg):
        os.makedirs(xdg, exist_ok=True)   
      if not os.path.exists(bootstrapper_desktop):
        f = open(bootstrapper_desktop, "w")
        f.write(bootstrapper_mime)
        f.close()
        # if this fails, install xdg-tools on your distrobution
        subprocess.call([
          "xdg-desktop-menu",
          "install",
          f"{bootstrapper_desktop}"
        ],
        subprocess.call(["update-desktop-database"])
        #stdout=subprocess.DEVNULL,
        #stderr=subprocess.STDOUT
        )
        
    case "Windows":
      import winreg
      print("") 