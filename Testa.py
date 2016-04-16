#import pytesseract

#from PIL import Image
#print pytesseract.image_to_string(Image.open("image.jpg"))


#from tesseract import image_to_string
#print image_to_string(Image.open('test.png'))
#print image_to_string(Image.open('test-european.jpg') lang='fra')
from PIL import Image
from pytesser import *
image = Image.open('fnord.tif')
# Open image object using PIL print image_to_string(image)
#  Run tesseract.exe on image fnord print image_file_to_string('fnord.tif') fnord ```