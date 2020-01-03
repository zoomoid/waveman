FROM python:3.7.6-buster

RUN apt-get update && apt-get install -y python3-dev libffi-dev cairo

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
