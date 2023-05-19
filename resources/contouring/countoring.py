import glob
import os
import cv2
import numpy as np
import math

def contour_cutter_circ(BP_images_dict, thrs=30, rplv=255):
    # Create list of circularity values
    circularity_list = []
    # Create list of masks
    masks = []

    for _, image in BP_images_dict["Source"]["B"].items():
        # Convert the color image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(f"Converted to grayscale")

        # Apply a binary threshold to the grayscale image
        _, threshold_mask = cv2.threshold(gray_image, thrs, rplv, cv2.THRESH_BINARY)
        print(f"Get threshold mask")

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

        # Calculate the area and perimeter of each contour
        try:
            areas = [cv2.contourArea(cnt) for cnt in contours]
        except Exception as e:
            print(e)
        perimeters = [cv2.arcLength(cnt, True) for cnt in contours]

        # Get the index of the contour with the largest area
        try:
            max_index = np.argmax(areas)
        except Exception as e:
            print(e)

        # Select the contour with the largest area
        max_contour = contours[max_index]

        # Calculate the circularity of the largest contour
        circularity = (4 * math.pi * areas[max_index]) / (perimeters[max_index] * perimeters[max_index])
        circularity_list.append(circularity)
        print(f"Roundness of contour: {circularity:.2f}")

        # Draw the largest contour on the mask, filled with white
        cv2.drawContours(mask, [max_contour], 0, (255, 255, 255), -1)

        # Append mask to list of masks
        masks.append(mask)

        # Apply the mask to the original color image
        result = cv2.bitwise_and(image, image, mask=mask)

    max_circularity = max(circularity_list)
    max_circularity_ind = circularity_list.index(max_circularity)
    # print(f"Max circularity = {max_circularity} in {img_list[max_circularity_ind]}")
    max_circularity_mask = masks[max_circularity_ind]
    return max_circularity_mask


def applying_mask(image, mask):
    cv2.bitwise_and(image, image, mask=mask)
    return image
