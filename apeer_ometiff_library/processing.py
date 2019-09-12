import itertools as it
import numpy as np
import skimage
from apeer_ometiff_library import io


def apply_2d_trafo(trafo_2d, array_5d, inputs):
    n_t, n_z, n_c, n_x, n_y = np.shape(array_5d)
    array_out_5d = None
    firstIteration = True

    for t, z, c in it.product(range(n_t), range(n_z), range(n_c)):
        result = trafo_2d(array_5d[t, z, c, :, :], inputs)
        if firstIteration:
            array_out_5d = np.zeros_like(array_5d, result.dtype)
            firstIteration = False
        array_out_5d[t, z, c, :, :] = result

    return array_out_5d


def apply_3d_trafo_zstack(trafo_3d, array_5d, inputs):
    n_t, n_z, n_c, n_x, n_y = np.shape(array_5d)
    array_out_5d = None
    firstIteration = True

    for t, c in it.product(range(n_t), range(n_c)):
        result = trafo_3d(array_5d[t, :, c, :, :], inputs)
        if firstIteration:
            array_out_5d = np.zeros_like(array_out_5d[t, :, c, :, :], inputs)
        firstIteration = False
        array_out_5d[t, :, c, :, :] = result

    return array_out_5d


def apply_3d_trafo_rgb(trafo_3d, array_5d, inputs):
    n_t, n_z, n_c, n_x, n_y = np.shape(array_5d)
    array_out_5d = None
    firstIteration = True

    for t, z in it.product(range(n_t), range(n_z)):
        result = trafo_3d(array_5d[t, z, :, :, :], inputs)
        if firstIteration:
            array_out_5d = np.zeros_like(array_out_5d[t, z, :, :, :], inputs)
        firstIteration = False
        array_out_5d[t, z, :, :, :] = result

    return array_out_5d

if __name__ == "__main__":
    path = ""
    (array5d, omexml) = io.read_ometiff(path)

    arrayOut5d = apply_2d_trafo(skimage.util.invert, array5d, None)

    io.write_ometiff("Test.ome.tiff", arrayOut5d, omexml)