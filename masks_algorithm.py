from abc import ABC, abstractmethod
import numpy
from skimage.morphology import flood_fill

class MaskAlgorithm(ABC):
    @abstractmethod
    def create_mask(self):
        pass


class CenteredMask(MaskAlgorithm):
    """Assumes the inside of the vertebra is centered so it starts the masking at the center of the img
    Black_limits needs to be set True
    """
    @staticmethod
    def create_mask(white_value, original_img):
        image = numpy.copy(original_img)
        x_value = int(image.shape[1] / 2)
        y_value = int(image.shape[0] / 2)
        image[y_value, x_value] = white_value
        image = flood_fill(image, (y_value, x_value, 0), white_value, tolerance=244.99)
        image[image < white_value] = 0
        return image