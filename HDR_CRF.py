import HDR_Aligning
import HDR_Test
import cv2
import HDR_Aligning
import HDR_CRF
import HDR_Merging
import HDR_Tonemaping
import LDR_Sharpening
import HDR_CRF_imp_export
import HDR_Saver
import Path_handler

def CRF_calculate(images_w_exposure, method="Debovec"):
    if isinstance(images_w_exposure, tuple):
        pass
    else:
        raise TypeError("Only tuple are allowed for 'images_w_exposure'")

    images, exposure_times = images_w_exposure

    try:
        print("Calculating Camera Response Function (CRF) ... ")

        if method == "Debovec":
            calibrateDebevec = cv2.createCalibrateDebevec()
            responseDebevec = calibrateDebevec.process(images, exposure_times)
        else:
            calibrateDebevec = cv2.createCalibrateRobertson()
            responseDebevec = calibrateDebevec.process(images, exposure_times)

    except Exception as e:
        print("Calculating CRF failed")
        print(e)
        return

    print("CRF calculation is complete")

    return responseDebevec

if __name__ == "__main__":
    cv_images, times = LDR_hist_equalizer.test_cv_images(selector="Img_test_", image_format="tiff")
    result_aligning = HDR_Aligning.aligning(cv_images, times)
    #CRF = CRF_calculate(result_aligning, method="Debovec")
    #HDR_CRF_imp_export.CRF_JSON_exporter(CRF, "./CRFs/CRF_Bottom.npy")
    CRF = HDR_CRF_imp_export.CRF_JSON_importer("./CRFs/CRF_B_100_4000_100_39.npy")
    result_merging = HDR_Merging.merging(result_aligning, CRF, selector="P")
    HDR_saver.HDR_saver(result_merging)
    result_merging = cv2.flip(result_merging, 0)
    result_tonemaping = HDR_Tonemaping.tonemaping(result_merging, selector="B")
    result_sharpening = LDR_Sharpening.LDR_sharpen(result_tonemaping)
    cv2.imwrite("test2.png", result_sharpening, [int(cv2.IMWRITE_PNG_COMPRESSION),0])