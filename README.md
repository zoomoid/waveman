# spectra-zoom

![Demo waveform visualization](demo/demo.png "Demo waveform visualization")

Generates visualizations of audio files like SoundCloud with some Python magic.

Requires `libsndfile` & `ffmpeg` to read audio format other than pure waves if used in host mode.

Otherwise just run the docker image and mount the audio file as volume.

```bash
usage: main.py [-h] [--input INPUT] [--steps STEPS] [--width WIDTH]
               [--height HEIGHT] [--output OUTPUT] [--color COLOR]
               [--rounded ROUNDED] [--mode MODE] [--align ALIGN]

optional arguments:
  -h, --help         show this help message and exit
  --input INPUT      Input file path. Required
  --steps STEPS      The total number of steps done. [Default 200]
  --width WIDTH      The total width of the image. [Default 2000]
  --height HEIGHT    The total height of the image. [Default 128]
  --output OUTPUT    Output file path. [Default $input]
  --color COLOR      The fill color for the bars. [Default 'black']
  --rounded ROUNDED  Rounded corner radius. [Default 0]
  --mode MODE        Sample visualization mode. Either 'avg' or 'max' [Default
                     'avg']
  --align ALIGN      Vertical bar alignment. Either 'center' or 'bottom'
                     [Default 'bottom']
```

## Docker Mode

Build the Docker image from the provided Dockerfile and run it like this 
```bash
$ docker build -t spectra-zoom:2.0 .
$ docker run -ti -v <Directory of audio file>:/spectra python3 main.py --input <Audio file> [ARGS...]
```