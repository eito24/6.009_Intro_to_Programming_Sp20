#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!

##
def get_pixel(result, x, y):
    if x<0:
        x=0
    elif x>=result.get('width'):
        x=result.get('width')-1
    if y<0:
        y=0
    elif y>=result.get('height'):
        y=result.get('height')-1
    return result['pixels'][(y*result.get('width'))+x]


def set_pixel(result, x, y, c):
    result['pixels'][(y*(result.get('width')))+x] = c


def apply_per_pixel(image, func):
    newpixels=[]
    for i in range(image.get('height')*image.get('width')):
        newpixels.append(0)
    result = {
        'height': image.get('height'),
        'width': image.get('width'),
        'pixels': newpixels,
    }
    for y in range(result.get('height')):
        for x in range(result.get('width')):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def correlate(image, kernel):
    newpixels=[]
    for i in range(image.get('height')*image.get('width')):
        newpixels.append(0)
    result = {
        'height': image.get('height'),
        'width': image.get('width'),
        'pixels': newpixels}

    kernel_height=int((len(kernel))**(1/2))
    kerneling_size=(kernel_height-1)//2
    def get_kern(kernel,x,y):
        return kernel[(y*kernel_height)+x]
    def set_new(result,x,y,c):
        result['pixels'][(y*(result.get('width')))+x] = c
    def kern_values(kernel):
        kernlist=[]
        for y in range(kernel_height):
            for x in range(kernel_height):
                kernlist.append(get_kern(kernel,x,y))
        return kernlist
    def pixel_values(image,x,y):
        pixellist=[]
        for n in range(-kerneling_size,kerneling_size+1):
            for m in range(-kerneling_size,kerneling_size+1):
                pixellist.append(get_pixel(image,m+x,n+y))
        return pixellist
    def summing(pixellist,kernlist):
        multiplied=[]
        summed=0
        for i in range(len(pixellist)):
            multiplied.append((pixellist[i])*(kernlist[i]))
        for i in range(len(pixellist)):
            summed=summed+multiplied[i]
        return summed

    for y in range(image.get('height')):
        for x in range(image.get('width')):
            set_new(result,x,y,summing(pixel_values(image,x,y),kern_values(kernel)))
    return result
    

    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    """
    raise NotImplementedError


def round_and_clip_image(image):
    newpixels=[]
    for i in range(image.get('height')*image.get('width')):
        newpixels.append(0)
    result = {
        'height': image.get('height'),
        'width': image.get('width'),
        'pixels': newpixels}
    for y in range(image.get('height')):
        for x in range(image.get('width')):
            if isinstance(get_pixel(image,x,y),int)==False:
                set_pixel(result,x,y,round(get_pixel(image,x,y)))
            if get_pixel(image,x,y)<0:
                set_pixel(result,x,y,0)
            elif get_pixel(image,x,y)>255:
                set_pixel(result,x,y,255)
    return result
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    raise NotImplementedError

def sharpblur(image, n):
    kernel=[]
    for i in range(n**2):
        kernel.append(1/(n**2))
    halfblur=correlate(image,kernel)
    return halfblur
# FILTERS

def blurred(image, n):
    return round_and_clip_image(sharpblur(image,n))
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    #raise NotImplementedError

    # then compute the correlation of the input image with that kernel
    #raise NotImplementedError

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    #raise NotImplementedError

def sharpened (image,n):
    newpixels=[]
    for i in range(image.get('height')*image.get('width')):
        newpixels.append(0)
    result = {
        'height': image.get('height'),
        'width': image.get('width'),
        'pixels': newpixels}
    blurry=sharpblur(image,n)
    for y in range(image.get('height')):
        for x in range(image.get('width')):
            set_pixel(result,x,y,((2*(get_pixel(image,x,y)))-(get_pixel(blurry,x,y))))
    return round_and_clip_image(result)

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES
def edges(image):
    newpixels=[]
    for i in range(image.get('height')*image.get('width')):
        newpixels.append(0)
    result = {
        'height': image.get('height'),
        'width': image.get('width'),
        'pixels': newpixels}
    kx=[-1, 0, 1, -2, 0, 2, -1, 0, 1]
    ky=[-1, -2, -1, 0, 0, 0, 1, 2, 1]
    finalox=correlate(image,kx)
    finaloy=correlate(image,ky)
    for y in range(image.get('height')):
        for x in range(image.get('width')):
            sqox=get_pixel(finalox,x,y)**2
            sqoy=get_pixel(finaloy,x,y)**2
            addxy=sqox+sqoy
            sqrtxy=addxy**(.5)
            set_pixel(result, x,y, sqrtxy)
    print(round_and_clip_image(result))
    return round_and_clip_image(result)



def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    a=load_image('test_images/centered_pixel.png')
    save_image(edges(a),'new_centered.png',mode='PNG')
    b=load_image('test_images/python.png')
    save_image(sharpened(b,11),'newpython.png',mode='PNG')      
    pass
