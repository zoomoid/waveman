import numpy as np
import librosa
import svgwrite
import argparse
import cairosvg

def max_in_area(y, j, delta):
  max = 0
  for i in range(j * delta, (j + 1) * delta):
    if abs(y[i]) > max:
      max = abs(y[i])
  return max

def create_buffer(data, delta, steps):
  samples = []
  for j in range(0, steps - 1):
    samples.append(max_in_area(data, j, delta))
  print('Created sample buffer')
  return samples

def draw(output_file, samples, step_width, step_height, color='white', gap=1, rounded=0):
  dwg = svgwrite.Drawing(output_file + '.svg')
  print('Drawing...')
  for i in range(0, len(samples)):
    dwg.add(dwg.rect(
      (i * (step_width) + gap, (1 - samples[i]) * step_height), # position
      (step_width - 0.5*gap, samples[i] * step_height), # size
      rounded, rounded, # border radius (x, y)
      fill=color)
    )

  dwg.save()
  print('Saved SVG.')

  cairosvg.svg2png(
    url=output_file + '.svg',
    write_to=output_file + '.png',
    parent_width=len(samples) * step_width + gap,
    parent_height=step_height,
    dpi=600,
    scale=1
  )
  print('Saved PNG.')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input', help='Input file path')
  parser.add_argument('--steps', help='The total number of steps done')
  parser.add_argument('--width', help='The total width of the image')
  parser.add_argument('--height', help='The total height of the image')
  parser.add_argument('--output', help='Output file path')
  parser.add_argument('--color', help="The fill color for the bars")
  parser.add_argument('--rounded', help="Rounded corner radius")
  args = parser.parse_args()

  if args.input:
    filename = args.input
  else:
    print('No input file provided, using first mp3 found in current folder')
    filename = './*.mp3'
  
  if args.output:
    output = args.output
  else:
    output = './' + filename

  if args.steps:
    steps = int(args.steps)
  else:
    steps = 200
  
  if args.width:
    step_width = int(args.width) / steps
  else:
    step_width = 2000 / steps

  if args.rounded:
    rounded = abs(int(args.rounded))
  else:
    rounded = 0

  if args.color:
    color = args.color
  else:
    color = "black"

  x_gap = 0.2 * step_width

  if args.height:
    step_height = int(args.height)
  else:
    step_height = 128
  
  print('Loading audio file into RAM...')
  print('Sampling at 48 kHz')
  y, sr = librosa.load(filename, 48000, True)
  print('Loaded and coverted audio to Mono track')

  delta_t = len(y) // steps
  samples = create_buffer(y, delta_t, steps)
  draw(
    output_file=output, 
    samples=samples,
    step_width=step_width, 
    step_height=step_height, 
    color=color, 
    gap=x_gap,
    rounded=rounded
  )

if __name__ == '__main__':
    main()