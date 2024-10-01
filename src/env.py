from types import SimpleNamespace

# hacky way to have an accesible dot attribute
app = SimpleNamespace(
  name = "hello",
  debug = False,
  baseurl = "http://tstblx.win"
)
discord = SimpleNamespace(
  client_id = 1243169469488959588,
)