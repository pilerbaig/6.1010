import pandas as pd
data = pd.read_csv("urop/Direc1AtT03000005000L0_corr3X3.csv")
#data = pd.read_csv("test_stuff.csv")


def get_val(datalist, dim, xind, yind, zind):
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
    # check if the pixel is within the image
    if not all(0 <= a < dim for a in [xind, yind, zind]):
        xind = get_index(dim, xind)
        yind = get_index(dim, yind)
        zind = get_index(dim, zind)
    # get the index of the pixel in the list
    index = xind * (dim ** 2) + yind * dim + zind
    # return the value of the desired pixel
    return datalist[index]


def get_index(dim, ind):
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
    return ind % dim


xind = 0
yind = 0
zind = 0
datalist = data['Phi'].tolist()
dim = int((len(datalist)+1) ** (1/3))
per_side = 1
indrange = range(0-per_side, dim+per_side)
philist = []
xlist = []
ylist = []
zlist = []
for newxind in indrange:
    xval = (newxind + per_side) * 0.05
    for newyind in indrange:
        yval = (newyind + per_side) * 0.05
        for newzind in indrange:
            zval = (newzind + per_side) * 0.05
            philist.append(
                get_val(datalist, dim, newxind, newyind, newzind))
            xlist.append(xval)
            ylist.append(yval)
            zlist.append(zval)
newdata = {'X': xlist,
           'Y': ylist,
           'Z': zlist,
           'Phi': philist, }
newdataframe = pd.DataFrame(newdata)
newdataframe.to_csv('Isotropic_extended.csv')

testlist = newdataframe['Phi'].tolist()

newdim = int((len(testlist)+1) ** (1/3))
# print(newdim)


#print(get_val(datalist, dim, 0, 0, 0))
#print(get_val(testlist, newdim, 130, 130, 130))
