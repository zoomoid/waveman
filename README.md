# SpectraZoom

Generates visualizations of audio files like SoundCloud with some Python magic.

Requires wave files for sampling.

Requires ``cairo` as graphics backend if used in host mode.
Otherwise just run the docker image and mount the audio file as volume.

```
usage: main.py [-h] [--input INPUT] [--steps STEPS] [--width WIDTH] [--height HEIGHT]
               [-output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  -input INPUT     Input file path
  --steps STEPS    The total number of steps done
  --width WIDTH    The total width of the image
  --height HEIGHT  The total height of the image
  -output OUTPUT   Output file path
```

```
python main.py --input '<audio file>' --width <WIDTH> --steps <STEPS> --height
<HEIGHT> -output '<output svg>'
```