from PIL import Image
import sys
import os
import tinify

TINIFY_API_KEY = 'The key can be obtained from https://tinypng.com/developers'

def cleanup(tmp_list):
    for t in tmp_list:
        os.remove(t)
    os.rmdir('tmp')

def file_walker():  
    in_tmp = [] 
    in_original = []
    PIL_images = []

    for r, d, f in os.walk(os.path.dirname(os.path.abspath(__file__))):
        for file in f:
            if ('.png' in file) or ('.jpg' in file):
                in_tmp.append(os.path.join(r, ('tmp/' + file)))
                in_original.append(os.path.join(r, file))
                PIL_images.append(Image.open(os.path.join(r, file)).convert('RGB'))
    return in_tmp, in_original, PIL_images


if len(sys.argv) < 2:
    print('Please include an output filename (e.g. output.pdf)')
    exit()
else:
    max_filesize = 0
    compress = False
    if len(sys.argv) > 2:
        if sys.argv[2].lower() == 'c':
            print(f'Compression argument detected, images will be temporarily compressed through the tinify API')
            compress = True
    print('Welcome to Images2PDF\nPlease put in the current folder all the images you want to merge into a PDF (images will be joined alphabetically)')


try:
    im_names_c, im_names, images = file_walker()

    if compress:
        os.mkdir('tmp')
        tin = tinify
        tin.key = TINIFY_API_KEY
        
        for i in range(len(im_names)):
            sys.stdout.write(f'\rCurrently compressing image {i + 1} out of {len(im_names) + 1}')
            sys.stdout.flush()

            source = tin.from_file(im_names[i])
            source.to_file(im_names_c[i])

        images = []
        for i in im_names_c:
            images.append(Image.open(i).convert('RGB'))
        cleanup(im_names_c)
    

    images[0].save(sys.argv[1], 'PDF', save_all=True, append_images=images[1:])
    print(f'\nPDF successfully generated with size {round(os.path.getsize(sys.argv[1]) / 1024 / 1024, 2)} MB')

except IndexError:
    print('! No images found in the current directory !')

