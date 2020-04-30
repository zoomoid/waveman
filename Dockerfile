FROM python:3.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libsndfile1-dev ffmpeg

ADD requirements.txt .

RUN pip3 install -r requirements.txt

ADD src src

ADD main.py .

ADD cli .

ADD config.json .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
