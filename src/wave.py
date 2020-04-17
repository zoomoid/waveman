import base64
import cairosvg
import svgwrite
import uuid
import librosa
from .logger import log
from .util import normalize, max_in_area, avg_in_area

"""
WaveMan module implementing a fluent API to use with an HTTP back-end

Example:

response = WaveMan(file_we_wrote_the_request_to, steps=50, step_width=32, height=320)
  .read().avg().normalize().draw() # read and process audio file to chunks
  .center(gap=1, color="#F58B44", rounded=16) # draw svg context
  .finish() # finish drawing
  .output().to_svg("name_of_svg").minify().to_png("name_of_png").to_base64() # write output files

NOTE that we require the to_svg and to_png functions to be provided with filenames including file endings!
"""
class WaveMan:
  samples = []
  chunks = []
  tmp_filename = None
  canvas = None
  def __init__(self, input_filename, steps=25, step_width=32, height=320):
    self.input = input_filename
    self.tmp_filename = str(uuid.uuid4())[0:7]
    self.steps = int(steps)
    self.step_width = float(step_width)
    self.height = int(height)
    log("Initializing new drawing context", temporary_filename=self.tmp_filename)
    self.canvas = svgwrite.Drawing(filename=self.tmp_filename)

  """
  Loads the audio file into the local buffer
  """
  def read(self):
    sr = 48000
    mono = True
    log("Loading audio file", sampling_rate=sr, mono=mono)
    samples, _ = librosa.load(self.input, sr, mono)
    self.samples = samples
    return self

  """
  Normalizes all currently generated chunks
  """
  def normalize(self):
    if not self.drawing:
      if len(self.chunks):
        self.chunks = normalize(self.chunks)
        return self
      else:
        raise FluentError("normalize_chunks only works on chunks, not on raw samples")
    else:
      raise FluentError("Cannot call normalize_chunks when already drawing")
    
  """
  Normalizes all currently loaded samples
  """
  def normalize_samples(self):
    if not self.drawing:
      self.samples = normalize(self.samples)
      return self
    else:
      raise FluentError("Cannot call normalize_samples when already drawing")
    
  """
  Generates averaged chunks for the currently loaded samples based on the given number of steps
  """
  def avg(self):
    if not self.drawing:
      log("Chose chunk generation mode", mode="avg")
      self.delta = len(self.samples) // self.steps
      for j in range(0, self.steps):
        self.chunks.append(avg_in_area(self.samples, j, self.delta))
    else:
      raise FluentError("Cannot call avg when already drawing")

  """
  Generates maximized chunks for the currently loaded samples based on the given number of steps
  """
  def max(self):
    if not self.drawing:
      log("Chose chunk generation mode", mode="max")
      self.delta = len(self.samples) // self.steps
      for j in range(0, self.steps):
        self.chunks.append(max_in_area(self.samples, j, self.delta))
    else:
      raise FluentError("Cannot call max when already drawing")

  """
  Starts the drawing phase
  """
  def draw(self):
    if len(self.chunks):
      log("Started drawing phase")
      self.drawing = True
      return self
    else:
      raise FluentError("Called draw before any chunks were generated")

  """
  Creates a drawer context with center alignment
  """
  def center(self):
    if self.drawing:
      log("Drawing center-aligned bars")
      return WaveManDrawerAlignBottom(self, self.canvas, self.chunks, self.step_width, self.height)
    else:
      raise FluentError("Cannot call bottom when not yet entered drawing mode")

  """
  Creates a drawer context with bottom alignment
  """
  def bottom(self):
    if self.drawing:
      log("Drawing bottom-aligned bars")
      return WaveManDrawerAlignBottom(self, self.canvas, self.chunks, self.step_width, self.height)
    else:
      raise FluentError("Cannot call bottom when not yet entered drawing mode")

  """
  Creates an Output object that can write SVG and PNG to disk and generate base64 encoded image data for usage in websites
  """
  def output(self):
    if self.chunks and self.canvas and self.tmp_filename:
      log("Requested output")
      return WaveManOutput(self.canvas, self.tmp_filename, (len(self.chunks) * self.step_width), self.height)
    else:
      raise FluentError("Called output before generating any processed data")

"""
Interface for Drawer backends
"""
class WaveManDrawer:
  def __init__(self, ctx, canvas, samples, step_width, height):
    self.ctx = ctx
    self.canvas = canvas
    self.samples = samples
    self.step_width = step_width
    self.height = height
  def finish(self):
    raise NotImplementedError

"""
Implementation of the Drawer for the bottom alignment of bars
"""
class WaveManDrawerAlignBottom(WaveManDrawer):
  """
  Actually draws a bottom-aligned waveform and returns the original WaveMan context
  """
  def finish(self, gap=1, rounded=0, color="white"):
    for i in range(0, len(self.samples)):
      pos = (i * (self.step_width),  (1 - self.samples[i]) * self.height)
      size = (self.step_width - gap, self.samples[i] * self.height)
      self.canvas.add(self.canvas.rect(pos, size, rounded, rounded, fill=color))
    log("Finished drawing", alignment="bottom", gap=gap, rounded=rounded, color=color)
    return self.ctx

"""
Implementation of the Drawer for the center alignment of bars
"""
class WaveManDrawerAlignCenter(WaveManDrawer):
  """
  Actually draws a center-aligned waveform and returns the original WaveMan context
  """
  def finish(self, gap=1, rounded=0, color="white"):
    for i in range(0, len(self.samples)):
      pos =  (i * (self.step_width), (0.5 * self.height) - (0.5 * self.samples[i] * self.height))
      size = (self.step_width - gap, self.samples[i] * self.height)
      self.canvas.add(self.canvas.rect(pos, size, rounded, rounded, fill=color))
    log("Finished drawing", alignment="center", gap=gap, rounded=rounded, color=color)
    return self.ctx

"""
WaveManOuput class to write output of wave-man to file and generate base64-encoded image data
"""
class WaveManOutput:
  tmp_filename = None
  rawSVGData = svgwrite.Drawing(filename='')
  exportedSVG = False
  exportedPNG = False
  png_filename = None
  svg_filename = None

  def __init__(self, rawSVG, tmp_filename, width, height):
    self.rawSVGData = rawSVG
    self.tmp_filename = tmp_filename
    self.width = width
    self.height = height

  """
  Writes the SVG to file in a human-readable format
  """
  def to_svg(self, filename):
    log("Requested SVG output", filename=filename, indent=2)
    self.svg_filename = filename
    self.rawSVGData.save(pretty=True, indent=2)
    self.exportedSVG = True
    return self

  """
  Writes the SVG to file, but minified
  """
  def minify_svg(self):
    if self.exportedSVG:
      log("Requested minified SVG output")
      self.rawSVGData.save(pretty=False)
      return self
    else:
      raise FluentError("Called minify before svg was exported")

  """
  Writes a PNG to file
  """
  def to_png(self, filename):
    if self.exportedSVG and self.svg_filename:
      self.png_filename = filename
      log("Requested PNG output", filename=filename)
      cairosvg.svg2png(
        url=self.svg_filename,
        write_to=self.png_filename,
        parent_width=self.width,
        parent_height=self.height,
        dpi=600,
        scale=1
      )
      self.exportedPNG = True
      return self
    else:
      raise FluentError("Called to_png before svg was exported")
    
  """
  Loads the generated PNG and returns it as base64-encoded image data
  """
  def to_base64(self):
    if self.exportedPNG and self.png_filename:
      log("Requested base64 representation of PNG", filename=self.png_filename)
      with open(self.png_filename, "rb") as f:
        data = f.read()
        return base64.b64encode(data)
    else:
      raise FluentError("Called to_base64 before byte image was exported")

"""
FluentError is a wave-man specific Error thrown wea
"""
class FluentError(RuntimeError):
  def __init__(self, message):
    self.message = message
