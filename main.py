import os
import uuid
import json
from requests import get as fetch
import fastapi
from pydantic import BaseModel
from waveman import WaveMan

app = fastapi.FastAPI()

class WaveBody(BaseModel):
    uri: str

"""
Expects a POST request with data 
"""
@app.post('/wavify')
def wavify(wave: WaveBody):
    print(wave.uri)
    # Generate random temporary file name 
    filename = str(uuid.uuid4())[0:8]
    # Download audio file
    response = fetch(wave.uri, timeout=30)
    print(response.status_code)
    if response.status_code == 200:
        with open(f"/app/tmp/{filename}.mp3", "wb") as f:
            print(f"/app/tmp/{filename}.mp3")
            f.write(response.content)
            f.close()
        # Generate SVG for sending back
        small_waveform = gen_small_waveform(filename)
        full_waveform = gen_full_waveform(filename)
        # cleanup afterwards
        os.unlink(f"/app/tmp/{filename}.mp3") 
        return {"full": full_waveform, "small": small_waveform}
    else:
        if response.status_code == 404:
            raise fastapi.HTTPException(status_code=404, detail="Audio file could not be found")
        else:
            raise fastapi.HTTPException(status_code=response.status_code)

def gen_full_waveform(filename):
    with open("config/full.json", "r") as f:
        full_config = json.load(f)
    waveman = WaveMan(f"/app/tmp/{filename}.mp3", config=full_config).run()
    svg = waveman.to_string()
    waveman = None
    return svg

def gen_small_waveform(filename):
    with open("config/small.json", "r") as f:
        small_config = json.load(f)
    waveman = WaveMan(f"/app/tmp/{filename}.mp3", config=small_config).run()
    svg = waveman.to_string()
    waveman = None
    return svg

@app.get('/healthz')
def health():
    return {"status": "ok"}

@app.get('/')
def root():
    return {"status": "ok"}