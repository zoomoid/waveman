import svgwrite
import soundfile
import os
import uuid
import json
from logger import log

from requests import get
from pydub import AudioSegment

CONFIG = {}

def waveman(fn, config=None):
  if config == None:
    with open("config.json", "r") as f:
      CONFIG = json.load(f)
  else:
    CONFIG = config
  CONFIG['width'] = CONFIG['steps'] * CONFIG['step_width']
  log("Initializing new drawing context", config=CONFIG)  
  canvas = svgwrite.Drawing(profile='tiny', viewBox=f"0 0 {CONFIG['width']} {CONFIG['height']}",
    preserveAspectRatio=CONFIG["preserveAspectRatio"])

  sf = soundfile.SoundFile(fn)
  total_samples = len(sf)
  block_length = int(total_samples // CONFIG['steps'])
  f = open(fn, "rb")
  block_iterator = soundfile.blocks(f, blocksize=block_length)
  chunks = []
  for i, block in enumerate(block_iterator):
    mono_block = list(map(lambda sample: (sample[0] + sample[1]) / 2, block))
    chunks += transformer(mono_block, CONFIG['mode'])

  chunks = normalize(chunks)
  for i, chunk in enumerate(chunks):
    canvas.add(artist(canvas, chunk, i, CONFIG['step_width'], CONFIG['height'], CONFIG['gap'], CONFIG['align'], CONFIG['rounded'], "#abcdef"))
  
  log("Tranformed samples into chunks")
  log("Created SVG rectangles for all data chunks")
  return canvas

def normalize(chunk):
  max_val = max([abs(s) for s in chunk])
  if max_val == 0:
    raise ArithmeticError
  return list(map(lambda v: v / max_val, chunk))

def transformer(chunk, mode):
  
  def avg(_chunk):
    return sum([abs(s) for s in _chunk]) / len(_chunk) 
  def rounded_avg(_chunk):
    return round(sum([abs(s) for s in _chunk]) / len(_chunk), 2)
  def max(_chunk):
    return max([abs(s) for s in _chunk])

  if mode == "max":
    chunk = max(chunk)
  elif mode == "avg":
    chunk = avg(chunk)
  elif mode == "rounded_avg":
    chunk = rounded_avg(chunk)
  else:
    raise TypeError

  return chunk

def artist(canvas, chunk, i, width, height, gap, align, rounded, color):
  def bottom(chunk, i):
    pos = (i * (width),  (1 - chunk) * height)
    size = (width - gap, chunk * height)
    return pos, size
  def center(chunk, i):
    pos =  (i * (width), (0.5 * height) - (0.5 * chunk * height))
    size = (width - gap, chunk * height)
    return pos, size
  if width == None or height == None or gap == None or align == None or rounded == None or color == None:
    raise TypeError
  log("Drawing chunk", i=i)
  if align == "bottom":
    pos, size = bottom(chunk, i)
  elif align == "center":
    pos, size = center(chunk, i)
  else:
    raise TypeError
  return canvas.rect(pos, size, rounded, rounded, fill=color)

def transcode(url, return_response=False):
  output_fn = str(uuid.uuid4())[0:8]
  with open(f"{output_fn}.mp3", 'wb') as f:
    r = get(url, timeout=1)
    f.write(r.content)
    f.close()
  sound = AudioSegment.from_mp3(f"{output_fn}.mp3")
  sound.export(f"{output_fn}.wav", format="wav")
  if return_response:
    return f"{output_fn}.wav", r
  else:
    return f"{output_fn}.wav"

def transcode_local(fn):
  output_fn = fn.replace(".mp3", "")
  sound = AudioSegment.from_mp3(f"{output_fn}.mp3")
  sound.export(f"{output_fn}.wav", format="wav")
  return f"{output_fn}.wav"

def to_string(canvas):
  return canvas.tostring().replace("#abcdef", "{{.color}}")

def cleanup(fn, clean_mp3=True, clean_wav=True):
  name = fn.replace(".wav", "") # strip extension from filename
  if clean_wav:
    os.unlink(f"{name}.wav")
  if clean_mp3:
    os.unlink(f"{name}.mp3")
  return True
