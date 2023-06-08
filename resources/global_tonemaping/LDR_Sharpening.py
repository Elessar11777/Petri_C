import cv2
from logger import aeya_logger


def LDR_sharpen(ldr_dict, iter=3, s=20, r=0.1):
    aeya_logger.info("Starting LDR sharpening")
    for light, image in ldr_dict.items():
        for i in range(iter):
            ldr_dict[light] = cv2.detailEnhance(image, sigma_s=s, sigma_r=r)
    aeya_logger.info("LDR is sharpened")
    return ldr_dict

