FROM python:3.7.6-slim

# RUN apt-get update && apt-get install -y python3-dev libffi-dev cairo

WORKDIR /spectra

RUN apt-get update && apt-get install -y libsndfile1-dev ffmpeg

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD main.py .

CMD ["/bin/bash"]
