import cv2
import numpy
from logger import aeya_logger

def merging(exp_img_dict, crf_dict):
    if isinstance(exp_img_dict, dict):
        pass
    else:
        raise TypeError("Only tuple are allowed for 'images_w_exposure'")
    if isinstance(crf_dict, dict):
        pass
    else:
        raise TypeError("Only numpy.ndarray are allowed for 'crf'")

    merging_dict = {}

    for light, exp_img in exp_img_dict.items():
        aeya_logger.info(f"Starting merging {light} images into one HDR image")
        exposure_list = []
        image_list = []
        for exposure, image in exp_img.items():
            exposure_list.append(exposure)
            image_list.append(image)

        exposure_list = numpy.array(exposure_list, dtype=numpy.float32)

        mergeDebevec = cv2.createMergeDebevec()
        merging_dict[light] = mergeDebevec.process(image_list, exposure_list, crf_dict[light])
        aeya_logger.info(f"Merging {light} complete")
    return merging_dict