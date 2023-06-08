import cv2
from logger import aeya_logger

def aligning(im_dict):
    """
    Function takes list of opencv images and returns them as list of aligned images
    :param im_dict: List of opencv images
    :return: Tuple of list of aligned opencv images and list of exposure times in numpy.ndarray
    """
    aeya_logger.info("Starting aligning")
    if isinstance(im_dict, dict):
        pass
    else:
        raise TypeError("Only lists are allowed for 'im_dict'")

    lights_dict = {
        "exposures": {
            "B": [],
            "P": []
        },
        "images": {
            "B": [],
            "P": []
        }
    }

    result_dict = {
            "B": [],
            "P": []
    }

    for light, dictionary in im_dict.items():
        for exposure, image in dictionary.items():
            lights_dict["exposures"][light].append(exposure)
            lights_dict["images"][light].append(image)

        alignMTB = cv2.createAlignMTB()
        alignMTB.process(src=lights_dict["images"][light], dst=lights_dict["images"][light])
        result_dict[light] = dict(zip(lights_dict["exposures"][light], lights_dict["images"][light]))

    aeya_logger.info("Aligning is complete")
    return result_dict

