from modules import *
img = Image.open("image.jpg")

yiq_pixels = rgb_to_yiq(img)
img2 = yiq_to_rgb(yiq_pixels)
img2.show()
