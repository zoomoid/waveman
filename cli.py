#!/usr/bin/python3
import argparse
from os import path
from logger import Logger
from waveman import waveman, transcode, to_string, cleanup
import timeit


def main():
    parser = argparse.ArgumentParser(
        description="Creates cool-lookin' audio waveform visualisations to use as assets in players and videos.")
    parser.add_argument(
        '--input', help='Input file path. Required', required=True, type=str)
    parser.add_argument(
        '--steps', help='The total number of steps done. [Default 64]', default=64, type=int)
    parser.add_argument(
        '--stepwidth', help='Width of each step. Can derive the total width by providing --steps and --stepwidth. [Default 45]', default=20, type=float)
    parser.add_argument(
        '--height', help='The total height of the image. [Default 300]', default=200, type=int)
    parser.add_argument(
        '--output', help='Output file path. [Default $input]', type=str)
    parser.add_argument(
        '--color', help="The fill color for the bars. [Default 'black']", default="black", type=str)
    parser.add_argument(
        '--rounded', help="Rounded corner radius. [Default 0]", default=20/2, type=float)
    parser.add_argument(
        '--mode', help="Sample visualization mode. Either 'avg' or 'max' [Default 'rounded_avg']", default="rounded_avg", type=str, choices=["avg", "max", "rnd_avg"])
    parser.add_argument(
        '--align', help="Vertical bar alignment. Either 'center' or 'bottom' [Default 'center']", default="center", type=str, choices=["bottom", "center"])
    args = parser.parse_args()

    if args.input:
        filename = args.input
    else:
        Logger.error("Missing input file")
        return
    if args.output:
        output = args.output
    else:
        output = './' + path.basename(filename).replace('.mp3', '')
    if args.steps:
        steps = int(args.steps)
    if args.stepwidth:
        step_width = int(args.stepwidth)
    if args.rounded:
        rounded = int(args.rounded)
    if args.color:
        color = args.color
    gap = 0.5 * step_width
    if args.height:
        height = int(args.height)
    if args.mode:
        if args.mode == "avg" or args.mode == "max" or args.mode == "rounded_avg":
            mode = args.mode
        else:
            Logger.warn("Found unsupported transformation mode. Only supports 'avg', 'rounded_avg' and 'max'", mode=args.mode)
            mode = "avg"
    if args.align:
        if args.align == "bottom" or args.align == "center":
            align = args.align
        else:
            Logger.warn("Found unsupported alignment. Only supports 'center' and 'bottom'", align=args.align)
            align = "center"

    config = {
        "align": align,
        "mode": mode,
        "step_width": step_width,
        "height": height,
        "rounded": rounded,
        "gap": gap,
        "steps": steps,
        "color": color,
        "sr": 48000,
        "scale": 1,
        "mono": True,
        "dpi": 600,
        "preserveAspectRatio": "none",
    }

    fn = transcode(filename)
    canvas = waveman(fn, config=config)
    svg = to_string(canvas)
    with open(f"{output}.svg", "w") as f:
        f.write(svg)
        f.close()
    cleanup(fn)

if __name__ == '__main__':
    timeit.timeit(lambda: main(), number=1)
