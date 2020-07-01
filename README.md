# wave-man

![Demo waveform visualization](demo/demo.png "Demo waveform visualization")

Generates visualizations of audio files like SoundCloud with some Python magic.

Requires `libsndfile` & `ffmpeg` to read audio formats other than pure waves if used in host mode.

Otherwise just run the docker image and mount the audio file as volume.

```bash
usage: main.py [-h] --input INPUT [--steps STEPS] [--totalwidth TOTALWIDTH]
               [--stepwidth STEPWIDTH] [--height HEIGHT] [--output OUTPUT]
               [--color COLOR] [--rounded ROUNDED] [--mode {avg,max}]
               [--align {bottom,center}]

Creates cool-lookin audio waveform visualisations to use as assets in players
and videos.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Input file path. Required
  --steps STEPS         The total number of steps done. [Default 200]
  --totalwidth TOTALWIDTH
                        The total width of the image. [Default 2000]
  --stepwidth STEPWIDTH
                        Width of each step. Can derive the total width by
                        providing --steps and --stepwidth. [Default 10]
  --height HEIGHT       The total height of the image. [Default 128]
  --output OUTPUT       Output file path. [Default $input]
  --color COLOR         The fill color for the bars. [Default 'black']
  --rounded ROUNDED     Rounded corner radius. [Default 0]
  --mode {avg,max,rounded_avg}      Sample visualization mode. Either 'avg', 'rounded_avg', or 'max'
                        [Default 'avg']
  --align {bottom,center}
                        Vertical bar alignment. Either 'center' or 'bottom'
                        [Default 'bottom']
```

## Docker Mode

Build the Docker image from the provided Dockerfile and run it like this 

```bash
# Build the Docker image yourself OR
$ docker build -t wave-man:latest src/

# Pull the official image from the Github Docker Registry
$ docker pull docker.pkg.github.com/occloxium/wave-man/wave-man:latest

# Run wave-man inside the image
$ docker run -ti -v <Directory of audio file>:/app/files python3 main.py --input <Audio file> [ARGS...]
```

## HTTP Server

Wave-Man is available as a standalone http backend that waits for an mp3 file to be submitted and returns SVG code according to the config.json file

Note that the URI has to be local, i.e., come from for example a mounted volume when running as a 
container or a valid filename for any mp3 located in ./files.

```
HTTP/1.1 POST /wavify {"uri": "<URL TO YOUR MP3>"}
```

