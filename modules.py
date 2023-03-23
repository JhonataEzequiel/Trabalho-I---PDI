from typing import List
from PIL import Image


def get_negative_pixels(image: Image = None) -> List:
    red_pixels = [[] for _ in range(image.size[0]-1)]
    green_pixels = [[] for _ in range(image.size[0]-1)]
    blue_pixels = [[] for _ in range(image.size[0]-1)]
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            colors = image.getpixel((r, c))
            red_pixels[r].append(255 - colors[0])
            green_pixels[r].append(255 - colors[1])
            blue_pixels[r].append(255 - colors[2])

    return [red_pixels, green_pixels, blue_pixels]


def turn_negative(image: Image = None):
    pixels = get_negative_pixels(image)
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            image.putpixel((r, c), (pixels[0][r][c], pixels[1][r][c], pixels[2][r][c]))
    return image


def rgb_to_yiq(image: Image = None):
    pixels = [[] for _ in range(image.size[0]-1)]
    for r in range(image.size[0]-1):
        for c in range(image.size[1]-1):
            colors = image.getpixel((r, c))
            y = 0.299*colors[0] + 0.587*colors[1] + 0.114*colors[2]
            i = 0.596*colors[0] - 0.274*colors[1] - 0.322*colors[2]
            q = 0.211*colors[0] - 0.523*colors[1] + 0.312*colors[2]
            pixels[r].extend([y, i, q])
    return pixels
