"""
AbstractConfig contains the general config settings that both, full and small share
"""
class AbstractConfig:
  def __init__(self, obj):
    self.step_width = obj["step_width"]
    self.height = obj["height"]
    self.rounded = obj["rounded"]
    self.steps = obj["steps"]
    self.gap = obj["gap"]
    self.width = obj["step_width"] * obj["steps"]

"""
Full is a config type for full waveforms
"""
class Full(AbstractConfig):
  pass

"""
Small is a config type for small waveforms
"""
class Small(AbstractConfig):
  pass

"""
Config contains both the full and the small config parsed from a given path to a json file
"""
class Config:
  def __init__(self, path="config/config.json"):
    with open(path, "r") as f:
      d = json.load(f)
    try:
      self._full = Full(d["full"])
      self._small = Small(d["small"])
    except AttributeError:
      raise AttributeError
  @property
  def full(self):
    return self._full
  @property
  def small(self):
    return self._small