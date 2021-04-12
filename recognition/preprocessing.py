import numpy as np


def normalize_input(image):
    """
    normalize image for face net input layer
    :param image:
    :return:
    """
    image = np.array(image)
    mean = np.mean(image)
    std = np.std(image)
    std_adj = np.maximum(std, 1.0 / np.sqrt(image.size))
    image = np.multiply(np.subtract(image, mean), 1 / std_adj)
    return image
