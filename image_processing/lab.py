"""
6.1010 Spring '23 Lab 1: Image Processing
"""

#!/usr/bin/env python3

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!


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
    return apply_per_pixel(image, lambda color: 255 - color)


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
    new_image = {"height": height, "width": width, "pixels": [0] * (width * height)}
    # get the size of the kernel
    kernel_size = int((len(kernel)) ** (1 / 2))
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
                check_pixel = get_pixel(image, check_row, check_col, boundary_behavior)
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
            (o_row["pixels"][i] ** 2 + o_col["pixels"][i] ** 2) ** (1 / 2)
        )
    # generate an image with the calculated pixels
    edges_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": edges_pixels,
    }
    # round and clip the new image
    round_and_clip_image(edges_image)
    # return the new image
    return edges_image


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
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
    by the "mode" parameter.
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

    # bluegill = load_greyscale_image("test_images/bluegill.png")
    # save_greyscale_image(inverted(bluegill), "bluegill_inverted.png")

    # kernel = [0] * 169
    # kernel[26] = 1
    # pigbird = load_greyscale_image("test_images/pigbird.png")
    # save_greyscale_image(correlate(pigbird, kernel, "zero"),
    #                      "pigbird_correlated_zero.png")
    # save_greyscale_image(correlate(pigbird, kernel, "extend"),
    #                      "pigbird_correlated_extend.png")
    # save_greyscale_image(correlate(pigbird, kernel, "wrap"),
    #                      "pigbird_correlated_warp.png")

    # cat = load_greyscale_image("test_images/cat.png")
    # save_greyscale_image(blurred(cat, 13), "cat_blurred.png")

    # python = load_greyscale_image("test_images/python.png")
    # save_greyscale_image(sharpened(python, 11), "python_sharpened.png")

    # centered_pixel = load_greyscale_image("test_images/centered_pixel.png")
    # save_greyscale_image(edges(centered_pixel), "isthisright.png")

    # construct = load_greyscale_image("test_images/construct.png")
    # save_greyscale_image(edges(construct), "construct_edges.png")
    im = load_greyscale_image("small_maze.png")
    print(im["pixels"])
    pass
