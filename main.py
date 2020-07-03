import os
import uuid
import json
import fastapi
from pydantic import BaseModel
from waveman import waveman, to_string, cleanup, transcode

app = fastapi.FastAPI()

class WaveBody(BaseModel):
  uri: str

"""
Expects a POST request with data 
"""
@app.post('/wavify')
def wavify(wave: WaveBody):
  fn = transcode(wave.uri)
  small_waveform = gen_waveform(fn, "config/small.json")
  full_waveform = gen_waveform(fn, "config/full.json")
  # cleanup afterwards
  cleanup(fn)
  return {
    "full": full_waveform,
    "small": small_waveform,
  }

def gen_waveform(filename, config_fn):
  with open(config_fn, "r") as f:
    cfg = json.load(f)
  wave = waveman(filename, config=cfg)
  svg = to_string(wave)
  wave = None
  return svg

@app.get('/healthz')
def health():
  return {"status": "ok"}

@app.get('/')
def root():
  return {"status": "ok"}