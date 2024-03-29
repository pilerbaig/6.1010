"""
6.1010 Spring '23 Lab 2: Image Processing 2
"""

#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image


# FUNCTIONS FROM PART 1

def get_pixel(image, row, col, boundary_condition="zero"):
    """
    Get the int value of a pixel given its row and column in the image.
    Does not modify inputs.

    Args:
        image: An image dictionary with three key/value pairs:
            * "height": an int representing the height in pixels
            * "width": an int representing the width in pixels
            * "pixels": a list of ints containing the pixels of the image
        row: an int representing the desired row of the pixel
        col: an int representing the desired column of the pixel
        boundary_condition: a string representing the desired method of
            getting pixels outside of the range of the image

    Returns:
        A new image dictionary.
    """
    # get the width and height of the image
    width = image["width"]
    height = image["height"]
    # check if the pixel is within the image
    if row < 0 or row > height - 1 or col < 0 or col > width - 1:
        # if the boundary condition is zero, return the value as 0
        if boundary_condition == "zero":
            return 0
        # if the boundary condition is extend, set the row and
        #   column to those given by the extend_index function
        elif boundary_condition == "extend":
            row = extend_index(height, row)
            col = extend_index(width, col)
        # if the boundary condition is extend, set the row and
        #   column to those given by the wrap_index function
        elif boundary_condition == "wrap":
            row = wrap_index(height, row)
            col = wrap_index(width, col)
    # get the index of the pixel in the list
    index = row * width + col
    # return the value of the desired pixel
    return image["pixels"][index]


def extend_index(dimension, index):
    """
    Get the dimension of a pixel outside an image using the extend method.
    Does not modify inputs.

    Args:
        dimension: an int representing the height/width of an image
        index: an int representing the row/column of a pixel

    Returns:
        A new index.
    """
    # set an index outside an image to the nearest index in the image and return it
    if index < 0:
        return 0
    elif index > dimension - 1:
        return dimension - 1
    else:
        return index


def wrap_index(dimension, index):
    """
    Get the dimension of a pixel outside an image using the wrap method.
    Does not modify inputs.

    Args:
        dimension: an int representing the height/width of an image
        index: an int representing the row/column of a pixel

    Returns:
        A new index.
    """
    # get the position of the pixel in one dimension
    #   corresponding to its position outside
    return index % dimension


def set_pixel(image, row, col, color):
    """
    Set a pixel in an image to the desired value.

    Args:
        image: An image dictionary with three key/value pairs:
            * "height": an int representing the height in pixels
            * "width": an int representing the width in pixels
            * "pixels": a list of ints containing the pixels of the image
        row: an int representing the desired row of the pixel
        col: an int representing the desired column of the pixel
        color: an int representing the desired color
    """
    # get the width of the image
    width = image["width"]
    # get the index of the pixel in the list
    index = row * width + col
    # change the value of the pixel at the desired index
    image["pixels"][index] = color


def apply_per_pixel(image, func):
    """
    Apply a function to each pixel in an image.
    Does not modify inputs.

    Args:
        image: An image dictionary with three key/value pairs:
            * "height": an int representing the height in pixels
            * "width": an int representing the width in pixels
            * "pixels": a list of ints containing the pixels of the image
        func: a function to be applied to each pixel
    """
    # generate a copy of the image
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"].copy(),
    }
    # iterate through rows and columns to get each pixel
    for col in range(image["width"]):
        for row in range(image["height"]):
            # get the color of the pixel
            color = get_pixel(image, row, col)
            # get the new color of the pixel
            new_color = func(color)
            # set the color of the pixel to the new color
            set_pixel(result, row, col, new_color)
    # return the resulting image
    return result


def inverted(image):
    """
    Invert the colors of an image

    Args:
        image: An image dictionary with three key/value pairs:
            * "height": an int representing the height in pixels
            * "width": an int representing the width in pixels
            * "pixels": a list of ints containing the pixels of the image

    Returns:
        A new image dictionary.
    """
    # apply a function inverting the color to each pixel and return the new image
    return apply_per_pixel(image, lambda color: 255-color)


# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior, clip=True):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    A kernel is represented by a string of ints the
        length of the total size of the kernel.
    """
    # return None if the boundary behavior specified is
    #   not one of the predetermined methods
    if boundary_behavior not in ["zero", "extend", "wrap"]:
        return None
    # get the height and width of the image
    height = image["height"]
    width = image["width"]
    # create a blank new image with the same dimensions
    new_image = {"height": height, "width": width,
                 "pixels": [0] * (width * height)}
    # get the size of the kernel
    kernel_size = int((len(kernel))**(1/2))
    # iterate through the rows and columns of the image
    for row in range(height):
        for col in range(width):
            # create an int to represent the value of the pixel
            new_pixel = 0
            # iterate through the kernel
            for kernel_entry in range(len(kernel)):
                # get the row and column of the kernel entry
                kernel_row = kernel_entry // kernel_size - kernel_size // 2
                kernel_col = kernel_entry % kernel_size - kernel_size // 2
                # get the row and column of the pixel in image being used
                check_row = row + kernel_row
                check_col = col + kernel_col
                # get the pixel being used
                check_pixel = get_pixel(
                    image, check_row, check_col, boundary_behavior)
                # add this value to the total value of the new pixel
                new_pixel += kernel[kernel_entry] * check_pixel
            # set the pixel in the new image to the value corresponding to the kernel
            set_pixel(new_image, row, col, new_pixel)
    # clip the image unless told not to
    if clip:
        round_and_clip_image(new_image)
    # return the new image
    return new_image


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    # iterate through the pixels in the image
    for i in range(len(image["pixels"])):
        # get the value of the pixel being checked
        pixel = image["pixels"][i]
        # round the pixel to an int
        pixel = round(pixel)
        # clip the pixel to 0 or 255 if it is outside of the range [0, 255]
        if pixel < 0:
            pixel = 0
        elif pixel > 255:
            pixel = 255
        # replace the pixel with the rounded and clipped value
        image["pixels"][i] = pixel


# FILTERS

def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel
    average_value = 1 / (kernel_size**2)
    kernel = [average_value] * kernel_size**2
    # then compute the correlation of the input image with that kernel
    new_image = correlate(image, kernel, "extend")
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(new_image)
    return new_image


def sharpened(image, kernel_size):
    """
    Return a new image representing the result of applying a sharpen filter (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # create a representation for the appropriate n-by-n kernel, the blur mask
    average_value = 1 / (kernel_size**2)
    kernel = [-average_value] * kernel_size**2
    # get the index of the midpoint pixel
    kernel_midpoint = kernel_size // 2 * kernel_size + kernel_size // 2
    # add 2 to the midpoint of the kernel to double the value of the pixel
    kernel[kernel_midpoint] += 2
    # compute the correlation of the input image with that kernel
    new_image = correlate(image, kernel, "extend")
    # round and clip the new image
    round_and_clip_image(new_image)
    # return the new image
    return new_image


def edges(image):
    """
    Emphasizes the edges of an image.
    Does not modify inputs.

    Args:
        image: An image dictionary with three key/value pairs:
            * "height": an int representing the height in pixels
            * "width": an int representing the width in pixels
            * "pixels": a list of ints containing the pixels of the image

    Returns:
        A new image dictionary.
    """
    # create the kernels to find the gradients
    k_row = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    k_col = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    # correlate the image with the gradient kernels without clipping
    o_row = correlate(image, k_row, "extend", False)
    o_col = correlate(image, k_col, "extend", False)
    # create an empty list to contain the list of new pixels
    edges_pixels = [0] * len(image["pixels"])
    # iterate through the indices of the image
    for i in range(len(edges_pixels)):
        # get the 2D gradient at each pixel and add it to the new list
        edges_pixels[i] = round(
            (o_row["pixels"][i] ** 2 + o_col["pixels"][i] ** 2) ** (1/2))
    # generate an image with the calculated pixels
    edges_image = {"height": image["height"],
                   "width": image["width"], "pixels": edges_pixels}
    # round and clip the new image
    round_and_clip_image(edges_image)
    # return the new image
    return edges_image

# VARIOUS FILTERS


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(image):
        """
        Given an image, returns an image with a filter applied.
        """
        # separate the colors of the image
        separated_colors = separate_colors(image)
        # filter each color separately
        red_filtered = filt(separated_colors[0])
        green_filtered = filt(separated_colors[1])
        blue_filtered = filt(separated_colors[2])
        # create a list to store the new pixels
        new_pixels = []
        # iterate through the filtered pixels and combine the filtered colors
        for i in range(len((red_filtered["pixels"]))):
            new_pixels.append(
                (red_filtered["pixels"][i], green_filtered["pixels"][i],
                 blue_filtered["pixels"][i]))
        # create a new image with the new pixels and return it
        new_image = {
            "height": image["height"],
            "width": image["width"],
            "pixels": new_pixels,
        }
        return new_image
    # return the new filter
    return color_filter


def separate_colors(image):
    """
    Given an image, return a tuple containing images of the red,
    green and blue values separately.
    """
    # create lists to store the pixels for each color
    red_list = []
    green_list = []
    blue_list = []
    # iterate through the colors in pixels and add each color to the corresponding list
    for _, color in enumerate(image["pixels"]):
        red_list.append(color[0])
        green_list.append(color[1])
        blue_list.append(color[2])
    # create an image from each color
    red_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": red_list,
    }
    green_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": green_list,
    }
    blue_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": blue_list,
    }
    # return the color images
    return (red_image, green_image, blue_image)


def make_blur_filter(kernel_size):
    """
    Given a kernel size, returns a function that applies a blur
    filter with the specified kernel size
    """
    def blur_color(image):
        """
        Given an image, returns an image with the blur filter applied.
        """
        return blurred(image, kernel_size)
    # return the new function
    return blur_color


def make_sharpen_filter(kernel_size):
    """
    Given a kernel size, returns a function that applies a sharpen
    filter with the specified kernel size
    """
    def sharpen_color(image):
        """
        Given an image, returns an image with the sharpen filter applied.
        """
        return sharpened(image, kernel_size)
    # return the new function
    return sharpen_color


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def cascade(image):
        """
        Given an image, returns a new image with filters applied.
        """
        new_image = image
        # for each filter in filters, apply it to the image and return it
        for filt in filters:
            new_image = filt(new_image)
        return new_image
    # return the filter cascade
    return cascade


# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    # create a new image that is a copy of the given image
    new_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"].copy(),
    }
    # perform the list of filters the number of times specified
    for _ in range(ncols):
        # take the greyscale of the image
        grey_image = greyscale_image_from_color_image(new_image)
        # compute the energy map of the greyscale image
        image_energy = compute_energy(grey_image)
        # compute the cumulative energy map of the energy map
        image_cem = cumulative_energy_map(image_energy)
        # find the lowest-energy seam
        image_seam = minimum_energy_seam(image_cem)
        # remove the seam from the image
        new_image = image_without_seam(new_image, image_seam)
    # return the final image
    return new_image

# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    # create a list to contain the new pixels
    new_pixels = []
    # iterate through the pixels
    for _, colors in enumerate(image["pixels"]):
        # add the grayscale version of the color pixel
        new_pixels.append(
            round(0.299*colors[0] + 0.587 * colors[1] + 0.114 * colors[2]))
    # create a new image with the new pixels and return it
    new_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": new_pixels,
    }
    return new_image


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    energy_image = edges(grey)
    return energy_image


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    # create a new image that is a copy of the given image
    new_image = {
        "height": energy["height"],
        "width": energy["width"],
        "pixels": energy["pixels"].copy(),
    }
    # get the dimensions of the image
    width = new_image["width"]
    height = new_image["height"]
    # iterate through each row and column
    for row in range(1, height):
        for col in range(width):
            # get the current pixel
            current_pixel = get_pixel(new_image, row, col)
            # check the adjacent pixels
            check_pixels = get_adjacent_pixels(new_image, row, col)
            # get the minimum of the adjacent pixels
            min_prev_pixel = min(check_pixels, key=lambda item: item[1])[1]
            # add this minimum to the current pixel
            new_pixel = current_pixel + min_prev_pixel
            # set the pixel to the new pixel
            set_pixel(new_image, row, col, new_pixel)
    # return the new image
    return new_image


def get_adjacent_pixels(image, row, col):
    """
    Given a color image and row and column dimensions, computes the
    adjacent pixels above it and their offset from the column.

    Returns a list of tuples including the offset and value of the adjacent pixels.
    """
    # create a list to contain the adjacent pixels
    adjacent_pixels = []
    # get the width of the image
    width = image["width"]
    # get the offset and value of the adjacent pixels, only for pixels within the image
    if col > 0:
        pixel_1 = (-1, get_pixel(image, row-1, col-1, "extend"))
        adjacent_pixels.append(pixel_1)
    pixel_2 = (0, get_pixel(image, row-1, col, "extend"))
    adjacent_pixels.append(pixel_2)
    if col < width:
        pixel_3 = (1, get_pixel(image, row-1, col+1, "extend"))
        adjacent_pixels.append(pixel_3)
    # return the list of adjacent pixels
    return adjacent_pixels


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    # get the dimensions of the cumulative energy map
    width = cem["width"]
    height = cem["height"]
    # create a list to contain the seam
    seam_list = []
    # get the index of the minimum value in the last row
    last_row = cem["pixels"][-width:]
    # get the dimensions of the minimum value
    col = last_row.index(min(last_row))
    row = height - 1
    # add the pixel to the seam
    seam_list.append(row * width + col)
    # iterate down through the remaining rows
    for row in range(height-2, -1, -1):
        # get the adjacent pixels
        check_pixels = get_adjacent_pixels(cem, row + 1, col)
        # get the offset for the minimum adjacent pixel
        col_offset = min(check_pixels, key=lambda item: item[1])[0]
        # compute the column of the minimum adjacent pixel
        col += col_offset
        # add the pixel to the seam
        seam_list.append(row * width + col)
    # reverse the seam so that it is in descending order
    seam_list.reverse()
    # return the seam
    return seam_list


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    # create an image that copies the given image
    new_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"].copy(),
    }
    # sort the seam from largest to smallest
    seam_sorted = list(sorted(seam, reverse=True))
    # remove each index from the seam
    for _, index in enumerate(seam_sorted):
        del new_image["pixels"][index]
    # fix the dimensions to account for removed pixels
    new_image["width"] -= 1
    # return the new image
    return new_image

# CUSTOM FEATURE


def custom_feature(image, x_offset, y_offset):
    """
    Given a (color) image and x and y offset ints, return a new image
    (without modifying the original) that creates a blue and red "3D glasses" effect.
    """
    # separate the colors of the image
    image_colors = separate_colors(image)
    # apply the "edges" filter for the red, blue and grayscaled image
    edge_red = edges(image_colors[0])
    edge_blue = edges(image_colors[2])
    edge_grey = edges(greyscale_image_from_color_image(image))
    # create a list to contain the new pixels
    new_pixel_list = []
    # shift the red and blue edge images by the given offsets
    offset_red = shift_image(edge_red, x_offset, y_offset)
    offset_blue = shift_image(edge_blue, -x_offset, -y_offset)
    # compute the new pixel given the red, blue, and grey images
    # softening the effect of the greyscale image
    for i in range(len(image["pixels"])):
        new_pixel_red = offset_red["pixels"][i] + \
            (edge_grey["pixels"][i]//4)
        new_pixel_green = edge_grey["pixels"][i]//4
        new_pixel_blue = offset_blue["pixels"][i] + \
            (edge_grey["pixels"][i]//4)
        new_pixel = (new_pixel_red, new_pixel_green, new_pixel_blue)
        # add the new pixel to the list
        new_pixel_list.append(new_pixel)
    # create the new image from the new pixels
    new_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": new_pixel_list,
    }
    # return the new image
    return new_image


def shift_image(image, x_offset, y_offset):
    """
    Given an image and x and y offset ints, return a new image
    (without modifying the original) that shifts the image by the specified amounts
    """
    # get the dimensions of the new image
    height = image["height"]
    width = image["width"]
    # create a new list to contain the offset pixels
    offset_pixels = []
    # add the pixel offset by the specified amounts to for each row and column
    for row in range(height):
        for col in range(width):
            offset_pixels.append(
                get_pixel(image, row - y_offset, col - x_offset, "extend"))
    # create a new image with the offset pixels
    new_image = {
        "height": height,
        "width": width,
        "pixels": offset_pixels,
    }
    # return the new image
    return new_image


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.

    # color_inverted = color_filter_from_greyscale_filter(inverted)
    # inverted_color_cat = color_inverted(
    #     load_color_image('test_images/cat.png'))
    # save_color_image(inverted_color_cat, "cat_inverted.png")

    # blur_filter = make_blur_filter(9)
    # color_blurred = color_filter_from_greyscale_filter(blur_filter)
    # blurry = color_blurred(load_color_image('test_images/python.png'))
    # save_color_image(blurry, "python_blurred.png")

    # sharpen_filter = make_sharpen_filter(7)
    # color_sharpened = color_filter_from_greyscale_filter(sharpen_filter)
    # sharp = color_sharpened(load_color_image('test_images/sparrowchick.png'))
    # save_color_image(sharp, "sparrowchick_sharpened.png")

    # filter1 = color_filter_from_greyscale_filter(edges)
    # filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    # filt = filter_cascade([filter1, filter1, filter2, filter1])
    # filtered_frog = filt(load_color_image('test_images/frog.png'))
    # save_color_image(filtered_frog, "frog_filtered.png")

    # twocats = load_color_image('test_images/twocats.png')
    # carved_twocats = seam_carving(twocats, 100)
    # save_color_image(carved_twocats, 'twocats_carved.png')

    # cat = load_color_image('test_images/cat.png')
    # custom_cat = custom_feature(cat, 5, -3)
    # save_color_image(custom_cat, 'custom_cat.png')
    pass
