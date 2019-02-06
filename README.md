# SpectraZoom

Generates visualizations of audio files like SoundCloud with some Python magic.

```
usage: main.py [-h] [-i I] [--steps STEPS] [--width WIDTH] [--height HEIGHT]
               [-o O]

optional arguments:
  -h, --help       show this help message and exit
  -i I             Input file path
  --steps STEPS    The total number of steps done
  --width WIDTH    The total width of the image
  --height HEIGHT  The total height of the image
  -o O             Output file path
```

```
python main.py -i '<audio file>' --width <WIDTH> --steps <STEPS> --height
<HEIGHT> -o '<output svg>'
```

To convert the SVG to PNG for further usage afterwards, I use ImageMagick like
that:

```
magick -quality 100 -background transparent -size <WIDTH>x<HEIGHT> <SVG FILE> <PNG FILE>
```

