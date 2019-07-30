from PIL import Image
import sys
import os


if len(sys.argv) < 2:
    print('Please include an output filename (e.g. output.pdf)')
    exit()
else:
    print('Welcome to Images2PDF\nPlease put in the current folder all the images you want to merge into a PDF (images will be joined alphabetically)')

path = os.path.dirname(os.path.abspath(__file__))
images = []


for r, d, f in os.walk(path):
    for file in f:
        if ('.png' in file) or ('.jpg' in file):
            im = Image.open(os.path.join(r, file))
            images.append(im.convert('RGB'))


try:
    images[0].save(sys.argv[1], 'PDF', resolution=100.0, save_all=True, append_images=images)
except:
    print('! No images found in the current directory !')

