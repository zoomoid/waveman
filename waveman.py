import base64
import cairosvg
import svgwrite
import uuid
import librosa
import json
from io import BytesIO
from logger import log
from util import normalize, max_in_area, avg_in_area

class WaveMan():
  samples = []
  chunks = []

  def __init__(self, audiofile, config=None):
    self.audiofile = audiofile
    if config == None:
      with open("config.json", "r") as f:
        self.config = json.load(f)
    else:
      self.config = config
    self.config['width'] = self.config['steps'] * self.config['step_width']
    log("Initializing new drawing context", config=self.config)  

  def run(self):
    self.canvas = svgwrite.Drawing(
      profile='tiny', viewBox=f"0 0 {self.config['width']} {self.config['height']}",
      preserveAspectRatio="none"
    )
    return self.load_audiofile()

  def load_audiofile(self):
    samples, _ = librosa.load(self.audiofile, self.config['sr'], self.config['mono'])
    self.samples = samples
    log("Loaded audio file", sampling_rate=self.config['sr'], mono=self.config['mono'])

    return self.transform()

  def transform(self):
    # def normalize_samples(self):
    #   self.samples = normalize(self.samples)
    def normalize_chunks(self):
      self.chunks = normalize(self.chunks)
    def avg(self, j):
      self.chunks.append(avg_in_area(self.samples, j, self.delta))
    def rounded_avg(self, j):
      digits = 2
      self.chunks.append(round(avg_in_area(self.samples, j, self.delta), digits))
    def max(self, j):
      self.chunks.append(max_in_area(self.samples, j, self.delta))
    
    self.delta = len(self.samples) // self.config['steps']
    log("Reducing sample array to chunks", mode=self.config['mode'])
    for j in range(0, self.config['steps']):
      if self.config['mode'] == "max":
        max(self, j)
      elif self.config['mode'] == "avg":
        avg(self, j)
      elif self.config['mode'] == "rounded_avg":
        rounded_avg(self, j)

    normalize_chunks(self)
    return self.draw()

  def draw(self):
    def bottom(self, i):
      pos = (i * (self.config['step_width']),  (1 - self.chunks[i]) * self.config['height'])
      size = (self.config['step_width']- self.config['gap'], self.chunks[i] * self.config['height'])
      return pos, size

    def center(self, i):
      pos =  (i * (self.config['step_width']), (0.5 * self.config['height']) - (0.5 * self.chunks[i] * self.config['height']))
      size = (self.config['step_width'] - self.config['gap'], self.chunks[i] * self.config['height'])
      return pos, size

    log("Drawing waveform", align=self.config['align'], radius=self.config['rounded'])
    for i in range(0, len(self.chunks)):
      if self.config['align'] == "bottom":
        pos, size = bottom(self, i)
      elif self.config['align'] == "center":
        pos, size = center(self, i)
      else:
        return
      self.canvas.add(self.canvas.rect(pos, size, self.config['rounded'], self.config['rounded'], fill=self.config['color']))

    log("Drawn bars onto canvas", "Chunks.length", len(self.chunks), "steps", self.config['steps'])
    self.chunks = []
    self.samples = []
    return self

  def to_string(self):
    return self.canvas.tostring()

  def to_png(self):
    return BytesIO(cairosvg.svg2png(bytestring=self.canvas.tostring().encode(), parent_width=self.config.width,
      parent_height=self.config.height, dpi=self.config.dpi, scale=self.config.scale
    ))
