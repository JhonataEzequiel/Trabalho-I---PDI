import os
import numpy as np
from modules import *

directory = "tests/"
test_image = directory+"image.jpg"

original_img = Image.open(test_image)
original_img.show(title="Original Image")

rgb_yiq_rgb = Image.open(test_image)
rgb_yiq_rgb = rgb_to_yiq(rgb_yiq_rgb)
rgb_yiq_rgb = yiq_to_rgb(rgb_yiq_rgb)
rgb_yiq_rgb.show(title="RGB to YIQ to RGB")

negative_img = Image.open(test_image)
negative_img = turn_negative(negative_img)
negative_img.show(title="Negative RGB")

negative_y = Image.open(test_image)
negative_y = negative_on_y(negative_y)
negative_y.show(title="Negative on Y")

median_3x3_extension = Image.open(test_image)
median_3x3_extension = median_ixj(3, 3, median_3x3_extension)
median_3x3_extension.show(title="Median 3x3 with extension")

median_7x7_extension = Image.open(test_image)
median_7x7_extension = median_ixj(7, 7, median_7x7_extension)
median_7x7_extension.show(title="Median 7x7 with extension")

# List all files in the directory
files = os.listdir(directory)

# Loop to verify if the file is a .txt
for file in files:
    # Verify if the file is a .txt
    if file.endswith(".txt"):
        image = correlational_filters(directory + file)
