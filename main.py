import os
import uuid
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
        waveman = WaveMan(f"/app/tmp/{filename}.mp3").run()
        svg = waveman.to_string()
        waveman = None
        # cleanup afterwards
        os.unlink(f"/app/tmp/{filename}.mp3") 
        return {"svg": svg}
    else:
        if response.status_code == 404:
            raise fastapi.HTTPException(status_code=404, detail="Audio file could not be found")
        else:
            raise fastapi.HTTPException(status_code=response.status_code)

@app.get('/healthz')
def health():
    return {"status": "ok"}

@app.get('/')
def root():
    return {"status": "ok"}