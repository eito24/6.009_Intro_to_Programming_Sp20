#!/usr/bin/env python3
#imported stuff
import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as Image


#obtains a pixel of coordinate (x,y) from an image (in this case result)
#the 'normal' format of get_pixel is (y*width)+x
#the if and elif statements account for out-of-image pixels, used in correlate
def get_pixel(result, x, y):
    if x<0:
        x=0
    elif x>=result['width']:
        x=result['width']-1
    if y<0:
        y=0
    elif y>=result['height']:
        y=(result['height'])-1
    return result['pixels'][(y*result['width'])+x]

#sets a pixel of image result at (x,y) to the value c
def set_pixel(result, x, y, c):
    result['pixels'][(y*(result['width']))+x] = c

#makes an image the size of image with all pixel values 0
def initial(image):
    newpixels=[]
    for i in range(image['height']*image['width']):
        newpixels.append(0)
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': newpixels,}
    return result

#applies the function func to every pixel in image
def apply_per_pixel(image, func):
    result=initial(image)
    for y in range(result['height']):
        for x in range(result['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result

#inverts the image
def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)

#takes an image and applies a kernel in the form of a list
def correlate(image, kernel):
    result=initial(image)
    #the kernel's physical height when not in a flat line, value should always be odd and the shape square
    kernel_height=int((len(kernel))**(1/2))
    #the number of pixels counting from the center that the kernel has an effect on (look at section 4)
    kerneling_size=(kernel_height-1)//2
    #makes a list out of the pixel values being affected by a kernel
    def pixel_values(image,x,y):
        pixellist=[]
        for n in range(-kerneling_size,kerneling_size+1):
            for m in range(-kerneling_size,kerneling_size+1):
                pixellist.append(get_pixel(image,m+x,n+y))
        return pixellist
    #makes a list of the modified pixellist in which the correlation function is done
    def summing(pixellist,kernel):
        multiplied=[]
        summed=0
        for i in range(len(pixellist)):
            multiplied.append((pixellist[i])*(kernel[i]))
            summed=summed+multiplied[i]
        return summed
    #makes a new image in which correlate has been acted on the original image
    for y in range(image['height']):
        for x in range(image['width']):
            set_pixel(result,x,y,summing(pixel_values(image,x,y),kernel))
    return result
    

    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE: A LIST
    """
    raise NotImplementedError
    ## what is this for

#just makes any pixel value below 0 into a 0 and any value above 255 a 255
def round_and_clip_image(image):
    result=initial(image)
    for y in range(image['height']):
        for x in range(image['width']):
            ##is there a better way to do this
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
#the kind of blurring that works for sharpened, doesn't do the clipping thing
def sharpblur(image, n):
    kernel=[]
    for i in range(n**2):
        kernel.append(1/(n**2))
    halfblur=correlate(image,kernel)
    return halfblur
#look at section 5.1, does sharpblur but w/ round&clip so is complete
def blurred(image, n):
    return round_and_clip_image(sharpblur(image,n))
#does a blur w/o round&clip, then performs a 2*I-B thing, section 5.2
def sharpened (image,n):
    result=initial(image)
    blurry=sharpblur(image,n)
    for y in range(image['height']):
        for x in range(image['width']):
            set_pixel(result,x,y,((2*(get_pixel(image,x,y)))-(get_pixel(blurry,x,y))))
    return round_and_clip_image(result)

#Does a Sobel Operatior, just follows formula
def edges(image):
    result=initial(image)
    kx=[-1, 0, 1,
        -2, 0, 2,
        -1, 0, 1]
    ky=[-1, -2, -1,
        0, 0, 0,
        1, 2, 1]
#first you correlate image with each of the kx and ky kernels
    finalox=correlate(image,kx)
    finaloy=correlate(image,ky)
#then square both, add, sqrt it, then make new image that has undergone such function
    for y in range(image['height']):
        for x in range(image['width']):
            sqox=get_pixel(finalox,x,y)**2
            sqoy=get_pixel(finaloy,x,y)**2
            addxy=sqox+sqoy
            sqrtxy=addxy**(.5)
            set_pixel(result, x,y, sqrtxy)
    return round_and_clip_image(result)


##not my stuff##
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

##not my stuff##
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

#just read the hashtagged description
if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.  
    pass
