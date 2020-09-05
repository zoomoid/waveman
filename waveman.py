import svgwrite
import soundfile
import os
import uuid
import json
from logger import Logger
from pydub import AudioSegment
from config import Config, Small, Full

class Position:
  def __init__(self, x, y)
    self._x = x
    self._y = y
  @property
  def x(self):
    return self._x
  @property 
  def y(self):
    return self._y

class Size:
  def __init__(self, w, h):
    self._w = w
    self._h = h
  @property
  def w(self):
    return self._w
  @property
  def h(self):
    return self._h

def waveman(fn, config=None):
  if config == None:
    with open("config.json", "r") as f:
      CONFIG = json.load(f)
  else:
    CONFIG = config
  CONFIG['width'] = CONFIG['steps'] * CONFIG['step_width']
  # log("Initializing new drawing context", file=fn)  
  canvas = svgwrite.Drawing(profile='tiny', viewBox=f"0 0 {CONFIG['width']} {CONFIG['height']}", preserveAspectRatio=CONFIG["preserveAspectRatio"])
  sf = soundfile.SoundFile(fn)
  total_samples = sf.frames
  block_length = int(total_samples // CONFIG['steps'])
  f = open(fn, "rb")
  block_iterator = soundfile.blocks(f, blocksize=block_length)
  chunks = []
  for i, block in enumerate(block_iterator):
    mono_block = list(map(lambda sample: abs((sample[0] + sample[1]) / 2), block))
    chunks.append(transformer(mono_block, CONFIG['mode'], block_length))
  chunks = normalize(chunks)
  # log("Tranformed frames into chunks")
  for i, chunk in enumerate(chunks):
    canvas.add(artist(canvas, chunk, i, CONFIG['step_width'], CONFIG['height'], CONFIG['gap'], CONFIG['align'], CONFIG['rounded'], "#abcdef"))
  # log("Created SVG rectangles for all data chunks")
  return canvas

"""
Normalizes a given list of numbers
"""
def normalize(l):
  m = max([abs(x) for x in l])
  return [x / m for x in l]

"""
Reduces a given chunk of samples according to a given mode, i.e.,
avg, max, and rounded_avg
"""
def transformer(chunk, mode, length):
  def avg(_chunk):
    return sum(_chunk) / length 
  def rounded_avg(_chunk):
    return round(sum(_chunk) / length, 3)
  def max(_chunk):
    return max(_chunk)

  if mode == "max":
    chunk = max(chunk)
  elif mode == "avg":
    chunk = avg(chunk)
  elif mode == "rounded_avg":
    chunk = rounded_avg(chunk)
  else:
    raise TypeError
  return chunk

"""
Transcodes an mp3 file located at vol/fn to a waveform which we can process using streams
""" 
def transcode(url):
  output_fn = str(uuid.uuid4())
  sound = AudioSegment.from_mp3(f"files/{url}")
  sound.export(f"/tmp/{output_fn}.wav", format="wav")
  Logger.info("Finished transcoding mp3 to wav", source=fn, target=f"{output_fn}.wav")
  return f"/tmp/{output_fn}.wav"

"""
Simply removes a file located at fn
"""
def cleanup(fn):
  os.unlink(fn)
  return True
