#!/usr/bin/env python3

import math

from PIL import Image



##copying from lab0##
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
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0]*image['height']*image['width']}
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
def load_greyscale_image(filename):
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
def save_greyscale_image(image, filename, mode='PNG'):
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

# VARIOUS FILTERS

def split_color_to_grey(image):
    red=[]
    green=[]
    blue=[]
    for i in range(len(image['pixels'])):
        red.append(image['pixels'][i][0])
        green.append(image['pixels'][i][1])
        blue.append(image['pixels'][i][2])
    red_image={'height':image['height'],'width':image['width'],'pixels':red}
    green_image={'height':image['height'],'width':image['width'],'pixels':green}
    blue_image={'height':image['height'],'width':image['width'],'pixels':blue}
    return (red_image, green_image, blue_image)
def combine_grey_to_color(tuple):
    new_color_image={'height':tuple[0]['height'],'width':tuple[0]['width'],'pixels':[]}
    for i in range(len(tuple[0]['pixels'])):
        new_color_image['pixels'].append((tuple[0]['pixels'][i],tuple[1]['pixels'][i],tuple[2]['pixels'][i]))
    return new_color_image

def color_filter_from_greyscale_filter(func):
    def filtering_separately(image):
        new_color_image=split_color_to_grey(image)
        red_filt=func(new_color_image[0])
        green_filt=func(new_color_image[1])
        blue_filt=func(new_color_image[2])
        filtered_color=combine_grey_to_color((red_filt,green_filt,blue_filt))
        return filtered_color
    return filtering_separately
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """


def make_blur_filter(n):
    def blurry_per_n(image):
        kernel=[]
        for i in range(n**2):
            kernel.append(1/(n**2))
        halfblur=correlate(image,kernel)
        return round_and_clip_image(halfblur)
    return blurry_per_n


def make_sharpen_filter(n):
    def sharpblur_per_n(image):
        kernel=[]
        for i in range(n**2):
            kernel.append(1/(n**2))
        halfblur=correlate(image,kernel)
        result=initial(image)
        for y in range(image['height']):
            for x in range(image['width']):
                set_pixel(result,x,y,((2*(get_pixel(image,x,y)))-(get_pixel(halfblur,x,y))))
        return round_and_clip_image(result)
    return sharpblur_per_n


def filter_cascade(list):
    def combined_filters(image):
        a=image
        for i in range(len(list)):
            a=list[i](a)
        return a
    return combined_filters
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """


# SEAM CARVING

# Main Seam Carving Implementation

def repeated_seaming(new_image,n):
    grey_image=greyscale_image_from_color_image(new_image)
    energy_map=compute_energy(grey_image)
    new_map=cumulative_energy_map(energy_map)
    delete_seam=minimum_energy_seam(new_map)
    new_image=image_without_seam(image,delete_seam)
    new_width=int(len(new_image['pixels'])/new_image['height'])
    new_image['width']=new_width
    return new_image
def seam_carving(image, ncols):
    new_image=image
    for _ in range(ncols):
        new_image=repeated_seaming(new_image,n)
    return new_image
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """


# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    grey_image=initial(image)
    for i in range(len(image['pixels'])):
        v=round((.299*image['pixels'][i][0])+(.587*image['pixels'][i][1])+(.114*image['pixels'][i][2]))
        grey_image['pixels'][i]=v
    return grey_image
    """
    Given a color image, computes and returns a corresponding greyscale image.
    Returns a greyscale image (represented as a dictionary).
    """

def compute_energy(grey_image):
    energy_map=edges(grey_image)
    return energy_map
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """

def min_adjacent_up(new_map,x,y):
    left_up=get_pixel(new_map,x-1,y-1)
    just_up=get_pixel(new_map,x,y-1)
    right_up=get_pixel(new_map,x+1,y-1)
    if x==0:
        a=min(just_up,right_up)
    elif x==new_map['width']-1:
        a=min(left_up,just_up)
    else:
        a=min(left_up,just_up,right_up)
    return a

def cumulative_energy_map(energy_map):
    new_map={
        'height': energy_map['height'],
        'width': energy_map['width'],
        'pixels': []}
    for y in range(energy_map['height']):
        for x in range(energy_map['width']):
            if y==0:
                new_map['pixels'].append(get_pixel(energy_map,x,y))
            else:
                to_add=min_adjacent_up(new_map,x,y)
                original=get_pixel(energy_map,x,y)
                cumulative_value=to_add+original
                new_map['pixels'].append(cumulative_value)
    return new_map
    """
    Given a measure of energy (e.g., the output of the compute_energy function),
    computes a "cumulative energy map" as described in the lab 1 writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
def min_adjacent_up2(new_map,x,y):
    left_up=get_pixel(new_map,x-1,y-1)
    just_up=get_pixel(new_map,x,y-1)
    right_up=get_pixel(new_map,x+1,y-1)
    if x==0:
        a=min(just_up,right_up)
    elif x==new_map['width']-1:
        a=min(left_up,just_up)
    else:
        a=min(left_up,just_up,right_up)
    if a==left_up:
        return(x-1,y-1)
    elif a==just_up:
        return(x,y-1)
    elif a==right_up:
        return(x+1,y-1)
def minimum_energy_seam(new_map):
    removing=[]
    ##appends bottom row minimum
    #bottom left corner is initial min
    lowest_position=(0,new_map['height']-1)
    for x in range(new_map['width']):
        if get_pixel(new_map,x,(new_map['height']-1))<get_pixel(new_map,lowest_position[0],lowest_position[1]):
            lowest_position=(x,new_map['height']-1)
    removing.append((lowest_position[1]*new_map['width'])+lowest_position[0])
    def next_pixel_up(x,y):
        wastepixel_loc=min_adjacent_up2(new_map,x,y)
        return (wastepixel_loc[0],wastepixel_loc[1])
    while lowest_position[1]>0:
        lowest_position=next_pixel_up(lowest_position[0],lowest_position[1])
        removing.append((lowest_position[1]*new_map['width'])+lowest_position[0])
    return removing
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 1 writeup).
    """
def image_without_seam(image, removing):
    new_image=image
    for i in removing:
        new_image['pixels'].pop(i)
    print(new_image)
    return new_image
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    pass

image= {'height': 5, 'width': 5, 'pixels': [
    1,1,1,1,0,
    1,1,1,0,1,
    1,1,1,1,0,
    1,0,1,1,1,
    0,1,1,1,0]}

a=seam_carving(image,2)
print (a)
