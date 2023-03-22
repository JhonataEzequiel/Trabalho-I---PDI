from typing import List
from PIL import Image


def get_negative_pixels(image: Image = None) -> List:
    red_pixels = [[] for _ in range(image.size[0]-1)]
    green_pixels = [[] for _ in range(image.size[0]-1)]
    blue_pixels = [[] for _ in range(image.size[0]-1)]
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            pixelColorVals = image.getpixel((r, c))
            red_pixels[r].append(255 - pixelColorVals[0])
            green_pixels[r].append(255 - pixelColorVals[1])
            blue_pixels[r].append(255 - pixelColorVals[2])

    return [red_pixels, green_pixels, blue_pixels]


def turn_negative(image: Image = None):
    pixels = get_negative_pixels(image)
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            image.putpixel((r, c), (pixels[0][r][c], pixels[1][r][c], pixels[2][r][c]))
    return image
