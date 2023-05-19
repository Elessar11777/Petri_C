import cv2

from resources.global_tonemaping import HDR_Aligning, HDR_CRF, HDR_Merging, HDR_Test, HDR_Tonemaping


def LDR_sharpen(img, selector="P", iter=3, s=20, r=0.1):

    for i in range(iter):
        if selector == "P":
            img = cv2.detailEnhance(img, sigma_s=s, sigma_r=r)

    return img

if __name__ == "__main__":
    cv_images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = HDR_Aligning.aligning(cv_images, times)
    CRF = HDR_CRF.CRF_calculate(result_aligning)
    result_merging = HDR_Merging.merging(result_aligning, CRF)
    result_tonemaping = HDR_Tonemaping.tonemaping(result_merging)
    result_sharpening = LDR_sharpen(result_tonemaping)

    print(result_sharpening)
    print(type(result_sharpening))