import librosa
import svgwrite
import argparse
import cairosvg
import time
import base64
import math
from os import path
from src.logger import log as logger
from src.waveman import WaveMan
from src.util import normalize, max_in_area, avg_in_area

"""
Slices the full samples list into smaller chunks and processes them based on the given mode

@param data full raw sample list
@param delta ratio of steps to total sample size
@param steps output chunks
@param mode string determining the processing mode. Currently supports "avg" and "max"
@return output chunk samples for drawing onto SVG canvas
"""
def create_buffer(data, delta, steps, mode="avg"):
  digits = 2
  samples = []
  logger("Creating chunks", steps=steps, mode=mode)
  for j in range(0, steps):
    if mode == "avg":
      samples.append(avg_in_area(data, j, delta))
    elif mode == "rnd_avg":
      samples.append(round(avg_in_area(data, j, delta), digits))
    elif mode == "max":
      samples.append(max_in_area(data, j, delta))
    else:
      raise "Unsupported mode"
    logger("Created chunk", chunk=j, value=samples[j])
  logger("Finished sample chunk creation", length=len(samples))
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
@param align baseline of alignment of boxes
"""
def draw(output_file, samples, step_width, step_height, color="white", gap=1, rounded=0, align="bottom"):
  dwg = svgwrite.Drawing(output_file + ".svg")
  logger("Start drawing boxes", boxes=len(samples), color=color, rounded_radius=rounded, align=align, gap=gap)
  for i in range(0, len(samples)):
    if align == "bottom":
      pos = (i * (step_width),  (1 - samples[i]) * step_height)
    elif align == "center":
      pos =  (i * (step_width), (0.5 * step_height) - (0.5 * samples[i] * step_height))
    else:
      logger("Found unsupported alignment", align=align)
      return
    
    dwg.add(dwg.rect(pos, (step_width - gap, samples[i] * step_height), rounded, rounded, fill=color)) # assuming top-left corner to bottom-right growth

  dwg.save()
  logger("Saved SVG to file", output=output_file, width=((step_width + gap) * len(samples)), height=step_height)

  cairosvg.svg2png(
    url=output_file + '.svg',
    write_to=output_file + '.png',
    parent_width=len(samples) * (step_width),
    parent_height=step_height,
    dpi=600,
    scale=1
  )
  
  logger("Converted SVG to PNG", output=output_file, width=((step_width + gap) * len(samples)), height=step_height)

def encode_as_base64(filename):
  with open(filename, "rb") as f:
    data = f.read()
    return base64.b64encode(data)
    

def main():
  parser = argparse.ArgumentParser(description="Creates cool-lookin' audio waveform visualisations to use as assets in players and videos.")

  parser.add_argument('--input', help='Input file path. Required', required=True, type=str)
  parser.add_argument('--steps', help='The total number of steps done. [Default 200]', default=200, type=int)
  parser.add_argument('--totalwidth', help='The total width of the image. [Default 2000]', default=2000, type=int)
  parser.add_argument('--stepwidth', help='Width of each step. Can derive the total width by providing --steps and --stepwidth. [Default 10]', default=10, type=float)
  parser.add_argument('--height', help='The total height of the image. [Default 128]', default=128, type=int)
  parser.add_argument('--output', help='Output file path. [Default $input]', type=str)
  parser.add_argument('--color', help="The fill color for the bars. [Default 'black']", default="black", type=str)
  parser.add_argument('--rounded', help="Rounded corner radius. [Default 0]", default=0, type=float)
  parser.add_argument('--mode', help="Sample visualization mode. Either 'avg' or 'max' [Default 'avg']", default="avg", type=str, choices=["avg", "max", "rnd_avg"])
  parser.add_argument('--align', help="Vertical bar alignment. Either 'center' or 'bottom' [Default 'bottom']", default="bottom", type=str, choices=["bottom", "center"])
  args = parser.parse_args()

  if args.input:
    filename = args.input
  else:
    logger("Missing input file")
    return
  
  if args.output:
    output = args.output
  else:
    output = './' + path.basename(filename)

  if args.steps:
    steps = int(args.steps)
  else:
    steps = 200

  if args.stepwidth:
    step_width = int(args.stepwidth)
  
  
  if args.totalwidth:
    step_width = int(args.totalwidth) / steps
  else:
    step_width = 2000 / steps
  
  if args.rounded:
    rounded = int(args.rounded)
  else:
    rounded = step_width / 2

  if args.color:
    color = args.color
  else:
    color = "black"

  x_gap = 0.1 * step_width

  if args.height:
    step_height = int(args.height)
  else:
    step_height = 128

  if args.mode:
    if args.mode == "avg" or args.mode == "max" or args.mode == "rounded_avg":
      mode = args.mode
    else:
      logger("Found unsupported transformation mode. Only supports 'avg', 'rounded_avg' and 'max'", mode=args.mode)
      mode = "avg"
  else:
    mode = "avg"
  
  if args.align:
    if args.align == "bottom" or args.align == "center":
      align = args.align
    else:
      logger("Found unsupported alignment. Only supports 'center' and 'bottom'", align=args.align)
      align = "bottom"
  else:
    align = "bottom"
  

  config = {
    "align": align,
    "mode": mode,
    "step_width": step_width,
    "height": step_height,
    "rounded": rounded,
    "gap": x_gap,
    "steps": steps,
    "color": color,
    "sr": 48000,
    "scale": 1,
    "mono": True,
    "dpi": 600,
  }

  WaveMan(filename, config)

  with open(f"{output}_base64.txt", "wb") as f:
    f.write(encode_as_base64(f"{output}.png"))
  
if __name__ == '__main__':
    main()