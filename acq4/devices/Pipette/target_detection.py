from __future__ import print_function
import numpy as np
import cv2
from skimage import measure
from scipy.ndimage import binary_fill_holes

class TargetDetector(object):
    def __init__(self, maskcnn, targetcnn):
        self.maskcnn = maskcnn
        self.targetcnn = targetcnn

    def findMask(self, image, threshold = 0.3):
        """Detect the target cell mask in *image* and return the mask as an array
         The *image* should have a size of 100x100 with pixel intensities scaled to (0,1)"""
        image = image.reshape([1, 100, 100])       
        predictedmask = self.maskcnn.predict(image)
        mask = self.cleanMask(predictedmask.reshape([100,100]), threshold = threshold)
        return mask
    
    def findLandingPos(self, image, mask):
        """Detect the target cell landing position in *image* and return the positions as an array
         The *image* should have a size of 100x100 with pixel intensities scaled to (0,1)
         The *mask* should be a 100x100 0/1 array 6y777777iuwith the cell-of-interest indicated by 1"""
        image = image.reshape([1, 100, 100, 1])
        mask = mask.reshape([1, 100, 100, 1])
        pos = self.targetcnn.predict([image, mask])
        return pos

    @staticmethod 
    def cleanMask(mask, threshold=0.3):
        _, binary_mask = cv2.threshold(mask, threshold, 1, cv2.THRESH_BINARY)
        labels = measure.label(binary_mask, connectivity=2)
        # Keep only the largest region
        if labels.max() != 0:  # Ensure at least one label was found
            largest_roi = labels == np.argmax(np.bincount(labels.flat)[1:]) + 1
            finalmask = binary_fill_holes(largest_roi*1)
        else:
            finalmask = labels # empty mask
        return finalmask
    
    @staticmethod
    def cropFrame(frame, expectedPos = None):
        image = frame.data()
        if expectedPos is None:
            height, width = len(image), len(image[0])
            expectedPos = [width//2, height//2]
        croppedimage = image[(expectedPos[0]-50):(expectedPos[0]+50), (expectedPos[1]-50):(expectedPos[1]+50)]        
        return croppedimage
    
    @staticmethod
    def scaleImage(image):
        min_val = np.min(image)
        max_val = np.max(image)
        scaledimage = (image - min_val) / (max_val - min_val)
        return scaledimage