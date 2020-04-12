FROM python:3.7.6

# RUN apt-get update && apt-get install -y python3-dev libffi-dev cairo

WORKDIR /spectra

ADD . .

RUN apt-get update 

RUN apt-get install -y libsndfile1-dev ffmpeg

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
