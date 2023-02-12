import numpy
import cv2

import HDR_Aligning
import HDR_Test
import HDR_CRF_imp_export

def merging(images_w_exposure, crf, selector="P"):
    if isinstance(images_w_exposure, tuple):
        pass
    else:
        raise TypeError("Only tuple are allowed for 'images_w_exposure'")

    if isinstance(crf, numpy.ndarray):
        pass
    else:
        raise TypeError("Only numpy.ndarray are allowed for 'crf'")

    cv_images, exposure_times = images_w_exposure

    if selector == "P":
        try:
            print("Merging perif images into one HDR image ... ")
            mergeDebevec = cv2.createMergeDebevec()
            hdrDebevec = mergeDebevec.process(cv_images, exposure_times, crf)
        except Exception as e:
            print("Merging failed")
            print(e)

        print("Merging complete")

    if selector == "B":
        try:
            print("Merging bottom images into one HDR image ... ")
            mergeDebevec = cv2.createMergeDebevec()
            hdrDebevec = mergeDebevec.process(cv_images, exposure_times, crf)
        except Exception as e:
            print("Merging failed")
            print(e)

        print("Merging complete")

    return hdrDebevec

if __name__ == "__main__":
    cv_images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = HDR_Aligning.aligning(cv_images, times)
    #CRF = HDR_CRF.CRF_calculate(result_aligning)
    CRF = HDR_CRF_JSON.CRF_JSON_importer('crf.json')
    print(CRF)
    print(merging(result_aligning, CRF))
    print(type(merging(result_aligning, CRF)))