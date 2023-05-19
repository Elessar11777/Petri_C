import cv2

from resources.global_tonemaping import HDR_Aligning, HDR_CRF, HDR_Merging
import HDR_Test


def HDR_saver(hdr, path):
    try:
        #cv2.imwrite(path, hdr)
        cv2.imwrite(path, cv2.cvtColor(hdr, cv2.COLOR_BGR2RGB))
        print(f"Saved HDR in {path}")
    except Exception as e:
        print("Saving failed")
        print(e)


if __name__ == "__main__":
    cv_images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = HDR_Aligning.aligning(cv_images, times)
    CRF = HDR_CRF.CRF_calculate(result_aligning)
    result_merging = HDR_Merging.merging(result_aligning, CRF)
    HDR_saver(result_merging)