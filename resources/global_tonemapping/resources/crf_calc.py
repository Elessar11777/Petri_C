import cv2
import numpy

def CRF_calculate(images_w_exposure):
    if isinstance(images_w_exposure, tuple):
        pass
    else:
        raise TypeError("Only tuple are allowed for 'images_w_exposure'")

    exposure_times, images = images_w_exposure
    exposure_times = numpy.float32(numpy.array(exposure_times))

    try:
        print("Calculating Camera Response Function (CRF) ... ")
        calibrateDebevec = cv2.createCalibrateDebevec()
        responseDebevec = calibrateDebevec.process(images, exposure_times)

    except Exception as e:
        print("Calculating CRF failed")
        print(e)
        return

    print("CRF calculation is complete")

    return responseDebevec