from types import SimpleNamespace

# hacky way to have an accesible dot attribute
app = SimpleNamespace(
  name = "hello",
  debug = False,
  baseurl = "http://localhost:8021"
)