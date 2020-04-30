FROM python:3.7

WORKDIR /app

RUN apt-get update && apt-get install -y libsndfile1-dev ffmpeg

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
