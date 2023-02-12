import numpy as np
import cv2

# image path


# Reading an image in default mode:
inputImage = cv2.imread("./11_45_05_P_kp3455-1.bmp")

# Remove small noise via median:
filterSize = 5
imageMedian = cv2.medianBlur(inputImage, filterSize)

# Get local maximum:
kernelSize = 15
maxKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
localMax = cv2.morphologyEx(imageMedian, cv2.MORPH_CLOSE, maxKernel, None, None, 1, cv2.BORDER_REFLECT101)

# Perform gain division
gainDivision = np.where(localMax == 0, 0, (inputImage/localMax))

# Clip the values to [0,255]
gainDivision = np.clip((255 * gainDivision), 0, 255)

# Convert the mat type from float to uint8:
gainDivision = gainDivision.astype("uint8")

# Convert RGB to grayscale:
grayscaleImage = cv2.cvtColor(gainDivision, cv2.COLOR_BGR2GRAY)

# Contrast Enhancement:
grayscaleImage = np.uint8(cv2.normalize(grayscaleImage, grayscaleImage, 0, 255, cv2.NORM_MINMAX))

cv2.imwrite("CLAHE image.png", grayscaleImage)


#cv2.imshow("Processed Image", grayscaleImage)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


