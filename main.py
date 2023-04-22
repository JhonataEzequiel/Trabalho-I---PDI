import numpy as np

from modules import *
"""original_img = Image.open("image.jpg")
original_img.show(title="Original Image")

rgb_yiq_rgb = Image.open("image.jpg")
rgb_yiq_rgb = rgb_to_yiq(rgb_yiq_rgb)
rgb_yiq_rgb = yiq_to_rgb(rgb_yiq_rgb)
rgb_yiq_rgb.show(title="RGB to YIQ to RGB")

negative_img = Image.open("image.jpg")
negative_img = turn_negative(negative_img)
negative_img.show(title="Negative RGB")

negative_y = Image.open("image.jpg")
negative_y = negative_on_y(negative_y)
negative_y.show(title="Negative on Y")

median_3x3_extension = Image.open("image.jpg")
median_3x3_extension = median_ixj(3, 3, median_3x3_extension)
median_3x3_extension.show(title="Median 3x3 with extension")

median_7x7_extension = Image.open("image.jpg")
median_7x7_extension = median_ixj(7, 7, median_7x7_extension)
median_7x7_extension.show(title="Median 7x7 with extension")
"""

with open("tests/box_11x11.txt") as f:
    lines = f.readlines()

correlational_filters = [line.strip() for line in lines]

offsets = [offset for offset in correlational_filters if ',' in offset]
offsets = [(int(offset.split(', ')[0]), int(offset.split(', ')[1]))
           for offset in offsets]

filters = [[] for _ in correlational_filters if ',' in _]

j = 0
for i in range(len(correlational_filters)):
    if correlational_filters[i] != '':
        filters[j].append(correlational_filters[i])
    if correlational_filters[i] == '':
        j += 1

finished_arrays = [_ for _ in range(len(filters))]
for j in range(len(filters)):
    filters[j].pop(0)
    for i in range(len(filters[j])):
        filters[j][i] = filters[j][i].split(' ')
        for h in range(len(filters[j][i])):
            treated_float = filters[j][i][h] if '/' in filters[j][i][h] else None
            if treated_float:
                split_float = filters[j][i][h].split('/')
                split_float = int(split_float[0])/int(split_float[1])
                filters[j][i][h] = split_float
        filters[j][i] = [float(_) for _ in filters[j][i]]

    finished_arrays[j] = np.array(np.array(filters[j]))

im = Image.open("tests/image.jpg")
for i in range(len(finished_arrays)):
    im = call_correlation_mxn(im, finished_arrays[i], offsets[i])

im.show()
im = histogram_expansion(im)
im.show()

f.close()
