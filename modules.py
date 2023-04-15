from typing import List
from PIL import Image, ImageOps
import numpy as np


def get_negative_pixels(image: Image = None) -> List:
    red_pixels = [[] for _ in range(image.size[0] - 1)]
    green_pixels = [[] for _ in range(image.size[0] - 1)]
    blue_pixels = [[] for _ in range(image.size[0] - 1)]
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
    y_pixels = [[_ for _ in range(image.size[1] - 1)] for _ in range(image.size[0] - 1)]
    i_pixels = [[_ for _ in range(image.size[1] - 1)] for _ in range(image.size[0] - 1)]
    q_pixels = [[_ for _ in range(image.size[1] - 1)] for _ in range(image.size[0] - 1)]
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            colors = image.getpixel((r, c))
            y = 0.299 * colors[0] + 0.587 * colors[1] + 0.114 * colors[2]
            i = 0.596 * colors[0] - 0.274 * colors[1] - 0.322 * colors[2]
            q = 0.211 * colors[0] - 0.523 * colors[1] + 0.312 * colors[2]
            y_pixels[r][c] = y
            i_pixels[r][c] = i
            q_pixels[r][c] = q
    return [y_pixels, i_pixels, q_pixels]


def get_rgb_pixels_from_yiq(pixels: List[List[List[float]]]):
    new_pixels = np.empty([len(pixels[0]), len(pixels[0][0]), 3], dtype=np.uint8)
    for i in range(len(pixels[0])):
        for c in range(len(pixels[0][0])):
            r = pixels[0][i][c] + 0.956 * pixels[1][i][c] + 0.621 * pixels[2][i][c]
            g = pixels[0][i][c] - 0.272 * pixels[1][i][c] - 0.647 * pixels[2][i][c]
            b = pixels[0][i][c] - 1.106 * pixels[1][i][c] + 1.703 * pixels[2][i][c]

            r = round(r)
            g = round(g)
            b = round(b)

            r = r if r > 0 else 0
            g = g if g > 0 else 0
            b = b if b > 0 else 0

            r = r if r < 256 else 255
            g = g if g < 256 else 255
            b = b if b < 256 else 255

            new_pixels[i][c] = np.array([r, g, b], dtype=np.uint8)

    return new_pixels


def yiq_to_rgb(pixels: List[List[List[float]]]):
    pixels = get_rgb_pixels_from_yiq(pixels)
    rotated_pixels = np.rot90(pixels, axes=(1, 0))
    new_image = Image.fromarray(rotated_pixels)
    return new_image


def negative_on_y(image: Image = None):
    yiq_pixels = rgb_to_yiq(image)
    for i in range(len(yiq_pixels[0])):
        for r in range(len(yiq_pixels[0][0])):
            yiq_pixels[0][i][r] = 255 - yiq_pixels[0][i][r]
    return yiq_to_rgb(yiq_pixels)


def median_ixj(i: int = 0, j: int = 0, image: Image = None, extension: bool = False):
    if i % 2 == 0 or j % 2 == 0:
        raise ValueError(" 'i' and 'j' must be odd")
    median_image = median_filter(image, (i, j), extension)

    return median_image


def median_filter(image: Image, size: tuple, zero_extension: bool = False):
    im = np.array(image)

    m, n = size
    window = np.ones((m, n))

    if zero_extension:
        result = np.zeros_like(im)
        offset = (m // 2, n // 2)
        padded_im = np.pad(im, offset, mode='constant')
        for i in range(im.shape[2]):
            for x in range(im.shape[0]):
                for y in range(im.shape[1]):
                    sub_image = padded_im[x: x + m, y: y + n, i]
                    result[x, y, i] = np.median(sub_image * window)
        result = np.uint8(result)

    else:
        result = np.zeros_like(im)
        for i in range(im.shape[2]):
            channel = im[:, :, i]
            padded_channel = np.pad(channel, (m // 2, n // 2), mode='edge')
            for x in range(im.shape[0]):
                for y in range(im.shape[1]):
                    sub_image = padded_channel[x: x + m, y: y + n]
                    result[x, y, i] = np.median(sub_image * window)
        result = np.uint8(result)

    return Image.fromarray(result)

