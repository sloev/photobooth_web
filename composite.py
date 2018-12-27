from PIL import Image
import os

MAX_COLUMNS = 5

INPUT_DIR = './segments/'
images = [Image.open(INPUT_DIR + filename) for filename in sorted(os.listdir(INPUT_DIR)) if filename.endswith('.png')]

MAX_ROWS = int(len(images)/MAX_COLUMNS) + (1 if len(images) % 20 !=0 else 0)

img_width, img_height = images[0].size
print(MAX_COLUMNS, MAX_ROWS, img_width,img_height)

background = Image.new('RGBA', ((img_width * MAX_COLUMNS) + img_width, (img_height * MAX_ROWS)), color='black')
bg_width, bg_height = background.size

x_index = 0
y_index = 0
column = 0
for index, image in enumerate(images):
    this_width = image.size[0]
    if x_index == 0:
        x_index = this_width
    background.paste(image, (x_index, y_index), image)
    
    x_index += this_width-20
    if x_index + img_width > bg_width:
        y_index += int(img_height - (img_height/2))
        column += 1
        x_index = int(this_width)

background.save("composite.png")