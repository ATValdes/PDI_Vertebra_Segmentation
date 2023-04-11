import masks_algorithm
from segmentation import SegmentationProcedure

WHITE_VALUE = 255
IMAGE_URL = 'images/'
FILE_NUMBER = 1
VERT_COUNT = 4
MASK_ALGORITHM = masks_algorithm.CenteredMask
BLACK_LIMITS = True

if __name__ == '__main__':
    SegmentationProcedure.start_segmentation(
        WHITE_VALUE,
        IMAGE_URL,
        FILE_NUMBER,
        MASK_ALGORITHM,
        BLACK_LIMITS,
        VERT_COUNT
        )
    print('Finished Segmentation.')