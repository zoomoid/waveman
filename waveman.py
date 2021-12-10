import svgwrite
import soundfile
import os
import uuid
import json
from logger import Logger
from pydub import AudioSegment
from config import Config, Small, Full
from artist import Artist
from transformer import Transformer

def waveman(fn, config=None):
  if config == None:
    with open("config.json", "r") as f:
      config = json.load(f)

  chunks = []
  Logger.info("Creating stream from wav", fn=fn)
  f = open(fn, "rb")
  with soundfile.SoundFile(fn, "rb") as f:
    block_length = int(f.frames // config.full.steps)
    chunks = Transformer(f, block_length, config.steps, chunk_window=2048, interpolation=16, mode="avg", mono=True).transform()
  Logger.info("Reduced and normalized audio chunks", chunks=len(chunks))
  """Generate lists of SVG strings for all audio chunks"""
  svg = Artist(chunks, config).to_string()
  return svg

"""
Transcodes an mp3 file located at vol/fn to a waveform which we can process using streams
""" 
def transcode(url):
  output_fn = str(uuid.uuid4())
  sound = AudioSegment.from_mp3(f"files/{url}")
  sound.export(f"/tmp/{output_fn}.wav", format="wav")
  Logger.info("Finished transcoding mp3 to wav", source=url, target=f"{output_fn}.wav")
  return f"/tmp/{output_fn}.wav"

"""
Simply removes a file located at fn
"""
def cleanup(fn):
  os.unlink(fn)
  return True
