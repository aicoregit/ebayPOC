#import cv2
#import numpy as np
#from matplotlib import pyplot as plt
#
#img = cv2.imread("/home/ubuntu/ebayPOC/static/abc.jpg")
#
#blur = cv2.blur(img,(100,100))
#
#cv2.imwrite("/home/ubuntu/ebayPOC/abc1.jpg",blur)

from PIL import Image, ImageFilter

img = Image.open("/home/ubuntu/ebayPOC/static/e3711700d8f02e6cb55dfed54fcbf674--office-kitchenette-kitchenette-ideas.jpg")

cropped_imge = img.crop((446,161,635,501))

blurred_image=cropped_imge.filter(ImageFilter.GaussianBlur(radius=5))
img.paste(blurred_image,(446,161,635,501))
img.save("/home/ubuntu/ebayPOC/cropped.jpg")