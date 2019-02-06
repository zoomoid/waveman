import numpy as np
import librosa
import svgwrite
import argparse

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

def draw(output_file, samples, step_width, step_height, color='black', gap=0):
  dwg = svgwrite.Drawing(output_file)
  print('Drawing...')
  for i in range(0, len(samples)):
    dwg.add(dwg.rect(
      (i * (step_width) + gap, (1 - samples[i]) * step_height), 
      (step_width - 0.5*gap, samples[i] * step_height), 
      fill=color)
    )

  dwg.save()
  print('Saved SVG.')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', help='Input file path')
  parser.add_argument('--steps', help='The total number of steps done')
  parser.add_argument('--width', help='The total width of the image')
  parser.add_argument('--height', help='The total height of the image')
  parser.add_argument('-o', help='Output file path')
  args = parser.parse_args()

  if args.i:
    filename = args.i
  else:
    print('No input file provided, using first mp3 found in current folder')
    filename = './*.mp3'
  
  if args.o:
    output = args.o
  else:
    output = './output.svg'

  if args.steps:
    steps = int(args.steps)
  else:
    steps = 200
  
  if args.width:
    step_width = int(args.width) / steps
  else:
    step_width = 2000 / steps

  x_gap = 0.2 * step_width

  if args.height:
    step_height = int(args.height)
  else:
    step_height = 128
  
  print('Loading audio file into RAM...')
  print('Sampling at 44.1 kHz')
  y, sr = librosa.load(filename, 44100, True)
  print('Loaded and coverted audio to Mono track')

  delta_t = len(y) // steps
  samples = create_buffer(y, delta_t, steps)
  draw(output, samples, step_width, step_height, 'black', x_gap)

if __name__ == '__main__':
    main()