import cv2

import HDR_Aligning
import HDR_Test
import HDR_CRF
import HDR_Merging
import HDR_Tonemaping
import LDR_Sharpening

def LDR_saver(ldr, path):
    try:
        cv2.imwrite(path, cv2.cvtColor(ldr, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        print(f"Saved {path}")
    except Exception as e:
        print("Saving failed")
        print(e)


if __name__ == "__main__":
    cv_images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = HDR_Aligning.aligning(cv_images, times)
    CRF = HDR_CRF.CRF_calculate(result_aligning)
    result_merging = HDR_Merging.merging(result_aligning, CRF)
    result_tonemaping = HDR_Tonemaping.tonemaping(result_merging)
    result_sharpening = LDR_Sharpening.LDR_sharpen(result_tonemaping)
    LDR_saver(result_sharpening)
