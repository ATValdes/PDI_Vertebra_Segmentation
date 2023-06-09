import os

import numpy
from skimage import io

from masks_algorithm import MaskAlgorithm


class ImageManager:
    def __init__(self, white_value = 255, x_value = 0, first_y = 1, second_y = 2) -> None:
        self.WHITE = white_value
        self.X_VALUE = x_value
        self.FIRST_Y = first_y
        self.SECOND_Y = second_y


class ImageAnalysis(ImageManager):
    def discover_edges(self, y_value: int, x_value: int, image: numpy.ndarray) -> list:
        """Grabs two values x and y, returns two edges allined with
        the x value in a list of the type: [x_value, first_y, second_y]"""
        discovered_edges = 0
        y_axis = y_value
        x_axis = x_value
        edges = [x_axis]
        while discovered_edges < 2 and y_axis < image.shape[0]:
            if image[y_axis, x_axis, 0] == self.WHITE:
                discovered_edges += 1
                edges.append(y_axis)
            y_axis += 1
        if discovered_edges == 2:
            return edges    

    def normalize_edges(self, left_edges: list, right_edges: list) -> None:
        if left_edges[self.FIRST_Y] > right_edges[self.FIRST_Y]:
            left_edges[self.FIRST_Y] = right_edges[self.FIRST_Y]
        elif left_edges[self.FIRST_Y] < right_edges[self.FIRST_Y]:
            right_edges[self.FIRST_Y] = left_edges[self.FIRST_Y]

        if left_edges[self.SECOND_Y] < right_edges[self.SECOND_Y]:
            left_edges[self.SECOND_Y] = right_edges[self.SECOND_Y]
        elif left_edges[self.SECOND_Y] > right_edges[self.SECOND_Y]:
            right_edges[self.SECOND_Y] = left_edges[self.SECOND_Y]


class ImageManipulation(ImageManager):
    def upper_pixels_black(self, x_value: int, y_value, image: int, black_limits: bool):
        """Make all pixels on top of the y value in the same column x black"""
        if black_limits == False:
            y_value -= 1  # In case the limit line must not be colored
        while y_value >= 0:
            image[y_value, x_value] = 0
            y_value -= 1

    def lower_pixels_black(self, x_value: int, y_value, image: int, black_limits: bool):
        """Make all pixels below the y value in the same column x black"""
        if black_limits == False:
            y_value += 1  # In case the limit line must not be colored
        while y_value < image.shape[0]:
            image[y_value, x_value] = 0
            y_value += 1

    def crop_image(self, left_edges: list, right_edges: list, upper_line_position: int, bottom_line_position: int, roi_image: numpy.ndarray, black_limits: bool):
        """
        Crops the image and sets the pixels past the upper and lower limits in black.
        """
        roi = numpy.copy(roi_image[left_edges[self.FIRST_Y]:right_edges[self.SECOND_Y] + 1, left_edges[self.X_VALUE]:right_edges[self.X_VALUE]])

        upper_limit_y = upper_line_position - left_edges[self.FIRST_Y]  # Calculates the new value for the position of the white line
        bottom_limit_y = bottom_line_position - left_edges[self.FIRST_Y]  # In the cropped image

        x_limit = roi.shape[1]
        x_value = 0
        
        
        while x_value != x_limit:
            if roi[upper_limit_y, x_value, 0] != self.WHITE:
                if roi[upper_limit_y + 1, x_value, 0] == self.WHITE:
                    upper_limit_y += 1
                elif roi[upper_limit_y - 1, x_value, 0] == self.WHITE:
                    upper_limit_y -= 1
            self.upper_pixels_black(x_value, upper_limit_y, roi, black_limits)
            x_value += 1
        x_value = 0
        while x_value != x_limit:
            if roi[bottom_limit_y, x_value, 0] != self.WHITE:
                if roi[bottom_limit_y - 1, x_value, 0] == self.WHITE:
                    bottom_limit_y -= 1
                elif roi[bottom_limit_y + 1, x_value, 0] == self.WHITE:
                    bottom_limit_y += 1
            self.lower_pixels_black(x_value, bottom_limit_y, roi, black_limits)
            x_value += 1
        return roi


class SegmentationProcedure:
    @staticmethod
    def start_segmentation(white_value:int, image_url:str, file_number:int, mask_algorithm:MaskAlgorithm, black_limits: bool, vert_count=4):
        roi_img = io.imread(f'{image_url}{file_number}_rois.tif')
        first_quarter = int(roi_img.shape[1] / 4)
        third_quarter = first_quarter * 3
        image_manipulation = ImageManipulation(white_value=white_value)
        image_analysis = ImageAnalysis(white_value=white_value)
        vert_number = 1
        yl_value_for_search = 0
        yr_value_for_search = 0

        while vert_number <= vert_count:
            left_edges = image_analysis.discover_edges(yl_value_for_search, first_quarter, roi_img)
            right_edges = image_analysis.discover_edges(yr_value_for_search, third_quarter, roi_img)

            yl_value_for_search = left_edges[2]  # Used to save where the last vert limit is so it keeps searching for
            yr_value_for_search = right_edges[2]  # the next one from there

            yl_value_for_crop = left_edges[1]  # Used to find the vert limits once the image is cropped
            yr_value_for_crop = left_edges[2]
            
            image_analysis.normalize_edges(left_edges, right_edges)
            vert_segmented = image_manipulation.crop_image(left_edges, right_edges, yl_value_for_crop, yr_value_for_crop, roi_img, black_limits)
            vert_mask = mask_algorithm.create_mask(white_value, vert_segmented)
            
            if not os.path.exists(f'images/{file_number}_segmented'):
                os.makedirs(f'images/{file_number}_segmented')

            io.imsave(f'images/{file_number}_segmented/L{vert_number}.tif', vert_segmented)
            io.imsave(f'images/{file_number}_segmented/L{vert_number}_mask.tif', vert_mask)
            
            vert_number += 1
            