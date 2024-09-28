import requests
import env
import args
import client

def get_latest_version():
  res = requests.get(f"{args.args.baseurl or env.app.baseurl}/api/v1/client/latest-version")
  return res.text

client_types = {
  "studio": 0,
  "player": 1,
}

def download_client(client_type = client_types["player"]):
  res = requests.get(f"{args.args.baseurl or env.app.baseurl}/api/v1/client/download/?type={client_type}")
  return res.text


def do():
  if get_latest_version() != client.get_version():
    download_client()