import librosa
import svgwrite
import argparse
import cairosvg
import time

"""
Small JSON logger using keyworded varargs

@param msg logger status message
@param **kwargs keyworded logger values
"""
def log(msg, **kwargs):
  log_obj = {}
  for key in kwargs:
    log_obj[key] = kwargs[key]
  log_obj['msg'] = msg
  print(f"{log_obj}")

"""
Absolute maximum mode:

For a given range, compute the absolute maximum sample
@param y - sample array
@param j - step index: means we compute for the j'th step
@param delta - range length
@return maximum absolute sample value
"""
def max_in_area(y, j, delta):
  return max([abs(y[i]) for i in range(j * delta, (j+1) * delta)])

"""
Average mode:

For a given range, compute the average sample
@param y - sample array
@param j - step index: means we compute for the j'th step
@param delta - range length
@return average sample value
"""
def avg_in_area(y, j, delta):
  return sum([abs(y[i]) for i in range(j * delta, (j+1) * delta)]) / delta 

"""
Normalizes a given list of numbers

@param y - list of numbers
"""
def normalize(y):
  max_val = max([abs(x) for x in y])
  return list(map(lambda v: v / max_val, y))

"""
Slices the full samples list into smaller chunks and processes them based on the given mode

@param data full raw sample list
@param delta ratio of steps to total sample size
@param steps output chunks
@param mode string determining the processing mode. Currently supports "avg" and "max"
@return output chunk samples for drawing onto SVG canvas
"""
def create_buffer(data, delta, steps, mode="avg"):
  samples = []
  log("Creating chunks", steps=steps, mode=mode)
  for j in range(0, steps):
    if mode is "avg":
      samples.append(avg_in_area(data, j, delta))
    elif mode is "max":
      samples.append(max_in_area(data, j, delta))
    else:
      raise "Unsupported mode"
    
  log("Finished sample chunk creation", length=len(samples))
  return normalize(samples)

"""
Draws the transformed sample list to a SVG canvas based on the given arguments

@param output_file filename for the output svg
@param samples transformed sample list
@param step_width horizontal length of bars
@param step_height vertical length of bars
@param color fill color for the bars. [Defaults to "white"]
@param gap spacing between the bars. [Defaults to 1]
@param rounded radius of rounded borders. Draws only symmetric, i.e., same y-radius as x-radius. [Defaults to 0] 
"""
def draw(output_file, samples, step_width, step_height, color='white', gap=1, rounded=0):
  dwg = svgwrite.Drawing(output_file + '.svg')
  log('Start drawing boxes', boxes=len(samples), color=color, rounded_radius=rounded)
  for i in range(0, len(samples)):
    dwg.add(dwg.rect(
      (i * (step_width) + gap, -0.5 * samples[i] + (0.5 * step_height)), # position
      (step_width - 0.5*gap, samples[i] * step_height), # size
      rounded, rounded, # border radius (x, y)
      fill=color)
    )

  dwg.save()
  log("Saved SVG to file", output=output_file, width=((step_width + gap) * len(samples)), height=step_height)

  cairosvg.svg2png(
    url=output_file + '.svg',
    write_to=output_file + '.png',
    parent_width=len(samples) * (step_width + gap),
    parent_height=step_height,
    dpi=600,
    scale=1
  )
  
  log("Converted SVG to PNG", output=output_file, width=((step_width + gap) * len(samples)), height=step_height)


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('--input', help='Input file path')
  parser.add_argument('--steps', help='The total number of steps done')
  parser.add_argument('--width', help='The total width of the image')
  parser.add_argument('--height', help='The total height of the image')
  parser.add_argument('--output', help='Output file path')
  parser.add_argument('--color', help="The fill color for the bars")
  parser.add_argument('--rounded', help="Rounded corner radius")
  parser.add_argument('--mode', help="Sample visualization mode. Either 'avg' or 'max' [Default 'avg']")

  args = parser.parse_args()

  if args.input:
    filename = args.input
  else:
    log("Missing input file")
    return
  
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
    rounded = int(args.rounded)
  else:
    rounded = 0

  if args.color:
    color = args.color
  else:
    color = "black"

  x_gap = 0.25 * step_width

  if args.height:
    step_height = int(args.height)
  else:
    step_height = 128

  if args.mode:
    mode = "avg"
  else:
    if args.mode is "avg" or args.mode is "max":
      mode = args.mode
    else:
      mode = "avg"
  
  start = time.time()

  log("Loading audio file into RAM", sampling_rate="48000", mono=True)

  y, sr = librosa.load(filename, 48000, True, )

  delta_t = len(y) // steps # delta is the ratio of desired steps (hence no. of bars) to the total sample count
  samples = create_buffer(y, delta_t, steps, mode=mode)
  draw(
    output_file=output, 
    samples=samples,
    step_width=step_width, 
    step_height=step_height, 
    color=color, 
    gap=x_gap,
    rounded=rounded
  )

  end = time.time()

  log("Finished processing the audio file", src=filename, target=output, time_taken=f"{round(end - start)} seconds")

if __name__ == '__main__':
    main()