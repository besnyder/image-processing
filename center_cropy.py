#!/usr/bin/env python3
"""
center_crop.py - Performs downscaling and center-crop of images in directory

Usage:
  center_crop.py <image_dir> <output_prefix> <resolution>
"""
import glob
import os
import pathlib
import sys
import traceback

from docopt import docopt
from PIL import Image, ImageOps


def parse_resolution_arg(resolution):
    try:
        if 'x' not in resolution:
            size = int(resolution)
            return size, size
        else:
            width, height = (int(s) for s in resolution.split('x'))
            return width, height
    except Exception:
        print("couldn't parse resolution.")


def main():
    args = docopt(__doc__, help=True)
    image_dir = args['<image_dir>']
    output_prefix = args['<output_prefix>']
    resolution = args['<resolution>']
    image_paths = glob.glob(image_dir + '/*.jpg')
    if len(image_paths) == 0:
        print('no images (or image directory) found.', file=sys.stderr)
        sys.exit(1)

    size = parse_resolution_arg(resolution)
    resolution = str(size[0]) + 'x' + str(size[1])
    output_dir = os.path.join(output_prefix, resolution)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    for img_path in image_paths:
        output_path = os.path.join(output_dir, os.path.basename(img_path))
        if os.path.exists(output_path):
            continue
        try:
            img = Image.open(img_path)
            img = ImageOps.fit(img, size, method=Image.BICUBIC)
            img.save(output_path)
        except Exception as e:
            tb = ''.join(traceback.format_exception(None, e, e.__traceback__))
            print('%s generated an exception, skipping: %s' % (img_path, tb))


if __name__ == '__main__':
    main()
