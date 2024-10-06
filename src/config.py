import executable
import log

import yaml
import sys
import os

class yaml_config:
  data = {}
  yaml_file = None
  template_data = {}

  def __init__(self):
    if os.path.exists(self.yaml_file):
      self.load()
      self.merge_dicts(self.template_data.copy(), self.data)
      self.save()
    else: 
      log.warn(f"no {os.path.basename(self.yaml_file)} found, creating file...")
      self.data = self.template_data
      self.save()

  def merge_dicts(self, source, target):
    for key, value in source.items():
      if isinstance(value, dict) and key in target:
        self.merge_dicts(value, target[key])
      elif key not in target:
        target[key] = value

  def get(self, *keys):
    data = self.data
    if len(keys) > 1:
      for key in keys:
        data = data[key]
    else:
      data = data[keys[0]]
    return data

  def set(self, keys, value):
    if len(keys) <= 0:
      return None
    data = self.data
    for key in keys[:-1]:
      if key not in data:
        data[key] = {}
      data = data[key]
    data[keys[-1]] = value
    self.save()
    return value

  def save(self):
    new_yaml = yaml.dump(self.data)
    new_file = open(self.yaml_file, "w")
    new_file.write(new_yaml)
    new_file.close()

  def load(self):
    f = open(self.yaml_file, "r")
    raw = f.read()
    self.data = yaml.safe_load(raw)
    f.close()

class bootstrapper_config(yaml_config):
  yaml_file = os.path.join(executable.path, "bootstrapper.yaml")
  template_data = {
    "baseurl": "http://www.tstblx.win",
    "debug": True,
    "discord": {
      "rpc": {
        "enabled": False
      }
    }
  }

 
class memory_config(yaml_config):
  yaml_file = os.path.join(executable.path, "memory.yaml")
  template_data = {
    "!": "DO NOT MODIFY!",
    "clients": {
      "player": {
        "version": ""
      },
      "studio": {
        "version": ""
      }
    }
  }
 
bootstrapper = bootstrapper_config()
memory = memory_config()