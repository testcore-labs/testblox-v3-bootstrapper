import executable
import config
import window
import client
import fetch
import log
import env

import requests
import os
import time
import sys
import zipfile
import shutil

download_path = os.path.join(executable.path, "clients")

def clean_tmp():
  tmp = os.path.join(download_path, "tmp")
  shutil.rmtree(tmp)

def extract_and_save(file_path, save_path, update_func=None):
  if not os.path.exists(os.path.dirname(save_path)):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

  with zipfile.ZipFile(file_path, 'r') as zip_file:
    file_list = zip_file.infolist()
    total_size = sum([file.file_size for file in file_list])
    downloaded = 0

    for file in file_list:
      zip_file.extract(file, save_path)
      downloaded += file.file_size
      if update_func:
        # hack!
        update_func(downloaded / 100, total_size)
    return save_path

def download_and_save(url, save_path, update_func=None):
  if not os.path.exists(os.path.dirname(save_path)):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

  if os.path.exists(save_path) and os.path.isfile(save_path):
    log.info(f"skipping downloaded file {os.path.basename(save_path)}")
    return # lets just skip downloading the same file okay?
  res = requests.get(url, stream=True)

  # express made me make a custom header
  total_size = int(res.headers.get("content-length") or res.headers.get("content-size"))
  # fast and works pretty well
  block_size = 80192

  downloaded = 0
  with open(save_path, "wb") as file:
    for data in res.iter_content(block_size):
      if not data:
        raise OSError("can't read block/chunk")
        break
      file.write(data)
      downloaded += len(data)
      if update_func:
        update_func(downloaded, total_size)

  return save_path

# unfortunately you'll have to change how this functions for specific revivals.
def download_client(latest_version, update_func = None):
  def progress_bar(downloaded, total): 
    if total > 0:
      progress = (int(downloaded) / int(total)) * 100
      progressbar = window.a.page("main").progressbar
      progressbar.stop()
      progressbar.configure(
        mode="determinate"
      )
      progressbar.set(progress)
    else:
      log.warn("there's something seriously wrong with the progress bar")
  window.a.page("main").progress_text.configure(text="downloading content.zip")
  contentzip = download_and_save(
    f"{fetch.baseurl}/api/v1/client/deploy/{latest_version}/content.zip",
    os.path.join(download_path, "tmp", latest_version, "content.zip"),
    progress_bar
  )
  window.a.page("main").progress_text.configure(text="downloading dlls.zip")
  dllszip = download_and_save(
    f"{fetch.baseurl}/api/v1/client/deploy/{latest_version}/dlls.zip",
    os.path.join(download_path, "tmp", latest_version, "dlls.zip"),
    progress_bar
  )
  window.a.page("main").progress_text.configure(text="downloading player.exe")
  playerexe = download_and_save(
    f"{fetch.baseurl}/api/v1/client/deploy/{latest_version}/player.exe",
    os.path.join(download_path, latest_version, "player.exe"),
    progress_bar
  )
  window.a.page("main").progress_text.configure(text="extracting content.zip")
  extract_and_save(
    os.path.join(download_path, "tmp", latest_version, "content.zip"),
    os.path.join(download_path, latest_version),
    progress_bar
  )
  window.a.page("main").progress_text.configure(text="extracting dlls.zip")
  extract_and_save(
    os.path.join(download_path, "tmp", latest_version, "dlls.zip"),
    os.path.join(download_path, latest_version),
    progress_bar
  )
  clean_tmp()
  window.a.page("main").progress_text.configure(text="done updating")
  config.memory.set(["clients", "player", "version"], latest_version)

  return


def do():
  latest_version = fetch.get_latest_version("player")
  if latest_version != client.get_version("player"):
    window.a.page("main").progress_text.configure(text="out of date, updating")
    log.info("outdated version, updating")

    download_client(latest_version)
  return