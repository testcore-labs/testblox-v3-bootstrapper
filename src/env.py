import time
from types import SimpleNamespace

# hacky way to have an accesible dot attribute
timings = SimpleNamespace(
  start = int(time.time())
)
app = SimpleNamespace(
  version = "1.0.0-beta",
  name = "testblox",
)
discord = SimpleNamespace(
  client_id = 1243169469488959588,
)