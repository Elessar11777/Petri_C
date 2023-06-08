import cv2
import numpy

from logger import aeya_logger

def CRF_calculate(images_w_exposure, method="Debovec"):
    aeya_logger.info("Starting CRF calculation")
    if isinstance(images_w_exposure, dict):
        pass
    else:
        raise TypeError("Only dict are allowed for 'images_w_exposure'")

    processing_dict = {
        "B": {
            "exposures": [],
            "numpy_exposures": numpy.zeros((100,)),
            "images": []
        },
        "P": {
            "exposures": [],
            "numpy_exposures": numpy.zeros((100,)),
            "images": []
        }
    }

    response_dict = {
        "B": "",
        "P": ""
    }
    try:
        for light, image_dict in images_w_exposure.items():
            for exposure, image in image_dict.items():
                processing_dict[light]["exposures"].append(exposure)
                processing_dict[light]["images"].append(image)

            processing_dict[light]["numpy_exposures"] = numpy.array(processing_dict[light]["exposures"], dtype=numpy.float32)

            if method == "Debovec":
                response_dict[light] = cv2.createCalibrateDebevec().process(processing_dict[light]["images"],
                                                                processing_dict[light]["numpy_exposures"])

            elif method == "Robertson":
                response_dict[light] = cv2.createCalibrateRobertson().process(processing_dict[light]["images"],
                                                                processing_dict[light]["numpy_exposures"])
    except Exception as e:
        aeya_logger.error("Calculating CRF failed")
        aeya_logger.error(e)
        return

    aeya_logger.info("CRF calculation is complete")

    return response_dict
