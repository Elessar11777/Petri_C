import glob
import os
import cv2
import numpy as np
import math


def contour_cutter_circ(b_img_list: list[np.ndarray], thrs: int = 15, rplv: int = 255):
    """
    Process a list of images, converting them to grayscale, thresholding, finding contours,
    and fitting ellipses to the largest contour.

    Args:
    - B_img_list (list): List of images to process.
    - thrs (int): Threshold value for binary thresholding.
    - rplv (int): Value to replace above the threshold.

    Returns:
    - list: List of masks with fitted ellipses drawn.
    """

    masks = []
    for image in b_img_list:

        # TODO: TEMP Multiply only for EF!!!
        image = (image * 255).astype(np.uint8)
        # Convert the color image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(f"Converted to grayscale")
        print(type(gray_image))

        # Apply a binary threshold to the grayscale image
        _, threshold_mask = cv2.threshold(gray_image, thrs, rplv, cv2.THRESH_BINARY)
        print(f"Get threshold mask")
        print(type(threshold_mask))

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(threshold_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"Get first contours")

        # Create a blank mask with the same dimensions as the grayscale image
        mask = np.zeros_like(gray_image)
        print(f"Created blank mask")

        # Draw the contours on the blank mask
        cv2.drawContours(mask, contours, -1, (255, 255, 255), 2)
        print(f"Contours drawn for mask")

        # Find contours again after drawing them on the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Reset the mask to blank
        mask = np.zeros_like(gray_image)

        try:
            # Calculate the area of each contour
            areas = [cv2.contourArea(cnt) for cnt in contours]

            # Get the index of the contour with the largest area
            max_index = np.argmax(areas)

            # Select the contour with the largest area
            max_contour = contours[max_index]

            # Fit an ellipse to the contour
            ellipse = cv2.fitEllipse(max_contour)
            # Draw the fitted ellipse on the mask
            cv2.ellipse(mask, ellipse, (255, 255, 255), -1)
        except Exception as e:
            print(e)

        return mask


def applying_mask(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)
