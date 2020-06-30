FROM tiangolo/uvicorn-gunicorn:python3.8-slim

WORKDIR /app

RUN apt-get update

RUN apt-get install -y libsndfile1 ffmpeg

ADD requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt

ADD . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]