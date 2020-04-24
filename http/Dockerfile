FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ADD main.py .

CMD [ "python3", "main.py"]
