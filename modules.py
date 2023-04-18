from typing import List
from PIL import Image
import numpy as np


def get_negative_pixels(image: Image = None) -> List:
    """
    This function returns every pixel in its negative counter-part.
    :param image: Original Image in RGB
    :return: List with the negative RGB pixels
    """
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
    """
    Transforms the image in its negative RGB counter-part
    :param image: Original image in RGB
    :return: New negative RGB image
    """
    pixels = get_negative_pixels(image)
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            image.putpixel((r, c), (pixels[0][r][c], pixels[1][r][c], pixels[2][r][c]))
    return image


def rgb_to_yiq(image: Image = None):
    """
    Receives an RGB image and makes the necessary adjusts to convert each pixel to its YIQ counter-part utilizing the
    correct formula for it.
    :param image: Original image in RGB
    :return: List containing every component of every pixel in YIQ format
    """
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
    """
    Similar to the RGB-YIQ function, but this time it does the opposite. It receives a list containing every pixel in
    YIQ format, and returns them in RGB format after conversion.
    :param pixels: List containing the pixels in YIQ format
    :return: np array containing every pixel in RGB format
    """
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
    """
    Transforms an image (in this case, it is a list of values that characterize a pixel) in YIQ into RGB calling an
    auxiliary function to make the calculations. It rotates the pixels as well to adjust the image correctly after the
    conversion.
    :param pixels: YIQ pixels list
    :return: RGB image from the YIQ pixels
    """
    pixels = get_rgb_pixels_from_yiq(pixels)
    rotated_pixels = np.rot90(pixels, axes=(1, 0))
    rotated_pixels = np.flip(rotated_pixels, axis=1)
    new_image = Image.fromarray(rotated_pixels)
    return new_image


def negative_on_y(image: Image = None):
    """
    Turns the Y from the YIQ color scheme into negative and returns an image of the result.
    :param image: Original image in RGB format
    :return: RGB image with the Y coordinate of YIQ negative.
    """
    yiq_pixels = rgb_to_yiq(image)
    for i in range(len(yiq_pixels[0])):
        for r in range(len(yiq_pixels[0][0])):
            yiq_pixels[0][i][r] = 255 - yiq_pixels[0][i][r]
    return yiq_to_rgb(yiq_pixels)


def median_ixj(i: int = 0, j: int = 0, image: Image = None, extension: bool = False):
    """
    Verifies if i and j are odd, and calls the function to apply the median filter. If i or j are odd, the function will
    raise an error.
    :param i: quantity of lines in the image
    :param j: quantity of columns in the image
    :param image: Original image in RGB format
    :param extension: boolean that says if the image will have zero extensions or not
    :return: new image with the filter applied.
    """
    if i % 2 == 0 or j % 2 == 0:
        raise ValueError(" 'i' and 'j' must be odd")
    median_image = median_filter(image, (i, j), extension)

    return median_image


def median_filter(image: Image, size: tuple, zero_extension: bool = False):
    """
    Applies the median filter to an image.
    :param image: original image in RGB format
    :param size: size of the median filter (ixj or mxn)
    :param zero_extension: boolean that says if it will have zero extension or not
    :return: new image with the filter applied.
    """
    im = np.array(image)

    m, n = size
    # window will be our kernel or 'mask', containing all values equals to 'one' and being m x n
    window = np.ones((m, n))

    if zero_extension:
        # the result variable will be initialized with zeros in the size of the original image
        result = np.zeros_like(im)
        # offset will determine how many zeros will be added to the edge of the image in order to extend it
        offset = (m // 2, n // 2)
        # padded_im will be the extended image with the necessary number of zeros. If it is not given a value to the
        # param 'constant_values', it will be zero, so the image will be extended by zeros
        padded_im = np.pad(im, offset, mode='constant')
        for i in range(im.shape[2]):
            for x in range(im.shape[0]):
                for y in range(im.shape[1]):
                    """
                    the sub_image will be the used to determine witch part of the image will be the one used to
                    calculate the median with the np.median function. The sub_image will be multiplied by the 'mask', in
                    this case, 'window', and passed as a parameter.
                    """
                    sub_image = padded_im[x: x + m, y: y + n, i]
                    result[x, y, i] = np.median(sub_image * window)
        # the final array will be converted to uint8 in order to use less memory
        result = np.uint8(result)

    else:
        # the result image will be initialized with zeros this time, and then it will be filled with the new image
        result = np.zeros_like(im)
        for i in range(im.shape[2]):
            # channel will have all the values of RGB in the image
            channel = im[:, :, i]
            # padded_channel will be used to apply the filter in the borders of the image as well
            padded_channel = np.pad(channel, (m // 2, n // 2), mode='edge')
            for x in range(im.shape[0]):
                for y in range(im.shape[1]):
                    sub_image = padded_channel[x: x + m, y: y + n]
                    result[x, y, i] = np.median(sub_image * window)
        result = np.uint8(result)

    return Image.fromarray(result)

