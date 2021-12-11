FROM python:3.10-bullseye

WORKDIR /app

RUN apt-get update

RUN apt-get install -y libsndfile1 ffmpeg

ADD requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt

ADD . .
