import cv2
import os
import numpy as np


INPUT_DIR = './images/'
OUTPUT_DIR = './segments/'
def filename_to_segmented(filename):
    img = cv2.imread(INPUT_DIR + filename)
    blured_img = cv2.medianBlur(img,5)
    _, thresh = cv2.threshold(blured_img,30,255,cv2.THRESH_BINARY)
    print(thresh.shape)
    print(img.shape)
    bg_color = np.array([  0,   0,   0], dtype=np.uint8)
    mask = np.all(thresh == bg_color, axis=2)

    img[mask] = [0, 0, 0]
    h,w,_ = img.shape

    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65), np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    rect = (2, 2, w-4, h-4)

    # Grabcut 
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    r_channel, g_channel, b_channel = cv2.split(img) 
    a_channel = np.where((mask==2)|(mask==0), 0, 255).astype('uint8')  

    img_RGBA = cv2.merge((r_channel, g_channel, b_channel, a_channel))[:, :w-100, :]
    output_filename = OUTPUT_DIR + filename.split('.', 1)[0] + '.png'

    # bg_color = np.array([  0,   0,   0, 255], dtype=np.uint8)

    # mask = np.all(img_RGBA == bg_color, axis=2)
    # img_RGBA[mask] = [0, 0, 0, 0]
    img_gray = cv2.cvtColor(img_RGBA, cv2.COLOR_BGR2GRAY)

    _,contours,_ = cv2.findContours(img_gray, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        # draw in blue the contours that were founded

        #find the biggest area
        c = max(contours, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(c)
        img_RGBA=img_RGBA[:, x:x+w]

        # draw the book contour (in green)
    cv2.imwrite(output_filename, img_RGBA)


for filename in os.listdir(INPUT_DIR):
    print(filename)
    filename_to_segmented(filename)