from modules import *
original_img = Image.open("image.jpg")
original_img.show(title="Original Image")

negative_img = Image.open("image.jpg")
negative_img = turn_negative(negative_img)
negative_img.show(title="Negative RGB")

negative_y = Image.open("image.jpg")
negative_y = negative_on_y(negative_y)
negative_y.show(title="Negative on Y")

median_3x3_no_extension = Image.open("image.jpg")
median_3x3_no_extension = median_ixj(3, 3, median_3x3_no_extension, False)
median_3x3_no_extension.show(title="Median 3x3 no extension")

median_3x3_extension = Image.open("image.jpg")
median_3x3_extension = median_ixj(3, 3, median_3x3_extension, True)
median_3x3_extension.show(title="Median 3x3 with extension")

median_7x7_no_extension = Image.open("image.jpg")
median_7x7_no_extension = median_ixj(7, 7, median_7x7_no_extension, False)
median_7x7_no_extension.show(title="Median 7x7 no extension")

median_7x7_extension = Image.open("image.jpg")
median_7x7_extension = median_ixj(7, 7, median_7x7_extension, True)
median_7x7_extension.show(title="Median 7x7 with extension")
