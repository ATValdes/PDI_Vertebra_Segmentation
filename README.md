# PDI Vertebra Segmentation - PDI Final

## Main Variables
* **White_value**: Determines the number considered true white.
* **Image_url**: Is the path where the DXA images will be read and stored.
* **File_number**: The file number that will be looked for in the designated path.

The complete url of an image would be like:
```
'{image_url}{file_number}_rois.tif
```
* **Vert_Count**: Number of vertebra that will be segmentated from the image.
* **Mask_Algorithm**: A class that contains the algorithm that will be used to look for the inside of the vertebra and generate the mask for each.
* **Black_LImits**: A boolean that decides if the limits of each vertebra are set to black before the masking process

## Masking Algorithm
If wanted to add a new mask generation algorithm, extend the abstract class *MaskAlgorithm* and add the new class in the *Mask_Algorithm* global variable in main.
For the moment, the is only one mask algorithm in the *mask_algorithm* file.

## Black Limits
In case there is a need to leave the limits of the vertebra white before the masking process, it can be done by changing the *Black_limits* global variable. Make sure few extra steps to paint the limits black during the masking process are done to ensure the masking is done correctly.