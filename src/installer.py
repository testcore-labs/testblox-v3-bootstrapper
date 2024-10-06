import uri_scheme
import executable
import client
import log

def installed():
  return uri_scheme.exists() and client.is_installed()

def install():
  if not executable.pyinstaller:
    log.throw("pyinstaller only")
  log.info("installing uri")
  uri_scheme.set_uri()
  
  