FROM python:3.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libsndfile1-dev ffmpeg

COPY requirements.txt .

ADD src src

RUN pip3 install -r src/requirements.txt

RUN pip3 install -r requirements.txt

ADD main.py .

CMD [ "python3", "main.py"]
