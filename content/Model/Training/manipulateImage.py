import cv2
import numpy as np
from random import randint, uniform
from PIL import Image, ImageEnhance

# crops image and then resizes it

def img_crop_black(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    # if it crops too much
    if(w < 10 or h < 10):
      y = 42
      w = 150
      x = 42
      h = 150
    crop = img[y:y+h,x:x+w]
    new_image_path = (image_path.split("/")[-1]).split(".")[0]
    new_image_path = "content/PillDataset/clean_data/" + new_image_path + ".jpg"
    cv2.imwrite(new_image_path ,crop)
    img_resize(new_image_path)
    
#resize image back to original
def img_resize(image_path): 
    src = image_path
    img = cv2.imread(cv2.samples.findFile(src), cv2.IMREAD_COLOR)
    height, width, channel = img.shape
    borderType = cv2.BORDER_CONSTANT
    # not guaranteed to be 224
    top = int((224 - height) / 2)
    bottom = top
    left = int((224 - width) / 2)
    right = left
    value = [randint(0, 255), randint(0, 255), randint(0, 255)]
    dst = cv2.copyMakeBorder(img, top, bottom, left, right, borderType, None, value)
    final = cv2.resize(dst, (224, 224))
    cv2.imwrite(src, final)


# def img_rotate(image_path):
#     img = Image.open(image_path)
#     rotate_angle = randint(-180, 180)
#     img_rotated = img.rotate(rotate_angle)
#     new_image_path = (image_path.split("/")[-1]).split(".")[0] + "_rotated.jpg"
#     img_rotated.save(new_image_path)
    
# def img_brightness(image_path):
#     img = Image.open(image_path)
#     enhancer = ImageEnhance.Brightness(img)
#     filter_val = uniform(0.55, 1.45)
#     img_brighten = enhancer.enhance(filter_val)
#     img_brighten.show()

    
# saturation 
# hue
# noise
# translation
