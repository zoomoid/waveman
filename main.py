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
  print(wave.uri)
  fn, response = transcode(wave.uri, return_response=True)
  if response.status == 200:
    # Generate SVG for sending back
    small_waveform = gen_small_waveform(fn)
    full_waveform = gen_full_waveform(fn)
    # cleanup afterwards
    cleanup(fn)
    return {"full": full_waveform, "small": small_waveform}
  else:
    if response.status == 404:
      raise fastapi.HTTPException(status_code=404, detail="Audio file could not be found")
    else:
      raise fastapi.HTTPException(status_code=response.status_code)

def gen_full_waveform(filename):
  with open("config/full.json", "r") as f:
    full_config = json.load(f)
  wave = waveman(filename, config=full_config)
  svg = wave.to_string()
  wave = None
  return svg

def gen_small_waveform(filename):
  with open("config/small.json", "r") as f:
    small_config = json.load(f)
  wave = waveman(filename, config=small_config)
  svg = waveman.to_string()
  wave = None
  return svg

@app.get('/healthz')
def health():
  return {"status": "ok"}

@app.get('/')
def root():
  return {"status": "ok"}