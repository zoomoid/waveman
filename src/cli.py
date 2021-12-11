#!/usr/bin/python3
import argparse
from os import path
import logging
from .config import (
    Artifact,
    ConfigurationManager,
)
from waveman import Waveman
import timeit


def main():
    parser = argparse.ArgumentParser(
        description="Creates cool-lookin' audio waveform visualisations to use as assets in players and videos."
    )
    parser.add_argument(
        "--input", help="Input file path. Required", required=True, type=str
    )
    parser.add_argument(
        "--steps", help="The total number of steps done", default=64, type=int
    )
    parser.add_argument(
        "--stepwidth",
        help="Width of each step. Can derive the total width by providing --steps and --stepwidth",
        default=20,
        type=float,
    )
    parser.add_argument(
        "--height", help="The total height of the image", default=200, type=int
    )
    parser.add_argument("--output", help="Output file path", type=str)
    parser.add_argument(
        "--color", help="The fill color for the bars", default="black", type=str
    )
    parser.add_argument(
        "--rounded", help="Rounded corner radius", default=20 / 2, type=float
    )
    parser.add_argument(
        "--mode",
        help="Sample visualization mode. Either 'avg', 'rounded_avg', or 'max'",
        default="rounded_avg",
        type=str,
        choices=["avg", "max", "rounded_avg"],
    )
    parser.add_argument(
        "--align",
        help="Vertical bar alignment. Either 'center' or 'bottom'",
        default="center",
        type=str,
        choices=["bottom", "center"],
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path to configuration file for additional, deeper configuration possibilities",
        default="center",
        type=str,
        choices=["bottom", "center"],
    )

    args = parser.parse_args()

    if args.input:
        filename = args.input
    else:
        logging.error("Missing input file")
        exit(1)

    if args.output:
        output = args.output
    else:
        output = path.curdir / path.basename(filename).replace(".mp3", "")

    single_artifact: Artifact = {
        "name": "cli",
        "configuration": {
            "steps": args.steps,
            "step_width": args.step_width,
            "height": args.height,
            "color": args.color,
            "rounded": args.rounded,
            "gap": 0.5 * args.step_width,
            "mode": args.mode,
            "align": args.align,
            "sr": 48000,
            "scale": 1,
            "mono": True,
            "dpi": 600,
            "preserveAspectRatio": "none",
        },
    }

    config_manager = ConfigurationManager(
        runtime_config=single_artifact,
    )

    wm = Waveman(audio_file=filename, config_manager=config_manager)

    wm.transcode().transform_all().draw_all().cleanup()

if __name__ == "__main__":
    timeit.timeit(lambda: main(), number=1)
