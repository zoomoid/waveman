FROM python:3.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libsndfile1-dev ffmpeg

ADD requirements.txt .

ADD src src

ADD main.py .

ADD config.json .

RUN pip3 install -r src/requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py"]
