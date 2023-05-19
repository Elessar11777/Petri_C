import cv2
import numpy

from resources.global_tonemaping import HDR_Aligning, HDR_CRF, HDR_Merging, HDR_Test


def tonemaping(hdr, selector="P", gb=1.4, sb=2.0, gp=1.6, sp=1.6):

    if selector == "B":
        tonemapped = cv2.createTonemapDrago(gamma=gb, saturation=sb)
        ldrDrago = tonemapped.process(hdr)
        ldrDrago = 3 * ldrDrago
        ldrDrago = numpy.clip(ldrDrago * 255, 0, 255).astype('uint8')
        invalid_indices = numpy.where((ldrDrago < 0) | (ldrDrago > 255))
        if invalid_indices[0].size > 0:
            print("Found invalid values at the following indices:", invalid_indices)
        else:
            print("No invalid values found.")
        ldrDrago[ldrDrago < 0] = 0
        ldrDrago[ldrDrago > 255] = 255

        return ldrDrago

    if selector == "P":
        tonemapped = cv2.createTonemapDrago(gamma=gp, saturation=sp)
        ldrDrago = tonemapped.process(hdr)
        ldrDrago = 3 * ldrDrago
        ldrDrago = numpy.clip(ldrDrago * 255, 0, 255).astype('uint8')

        invalid_indices = numpy.where((ldrDrago < 0) | (ldrDrago > 255))
        if invalid_indices[0].size > 0:
            print("Found invalid values at the following indices:", invalid_indices)
        else:
            print("No invalid values found.")
        ldrDrago[ldrDrago < 0] = 0
        ldrDrago[ldrDrago > 255] = 255

        return ldrDrago



if __name__ == "__main__":
    cv_images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = HDR_Aligning.aligning(cv_images, times)
    CRF = HDR_CRF.CRF_calculate(result_aligning)
    result_merging = HDR_Merging.merging(result_aligning, CRF)
    result_tonemaping = tonemaping(result_merging)

    print(result_tonemaping)
    print(type(result_tonemaping))