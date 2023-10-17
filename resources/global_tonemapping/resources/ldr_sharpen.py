import cv2

def LDR_sharpen(img, selector="P", iter=3, s=20, r=0.1):

    for i in range(iter):
        if selector == "P":
            img = cv2.detailEnhance(img, sigma_s=s, sigma_r=r)

    return img
