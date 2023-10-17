import numpy
import cv2

def merging(images_w_exposure, crf):

    exposure_times, cv_images = images_w_exposure
    exposure_times = numpy.float32(numpy.array(exposure_times))
    try:
        print("Merging perif images into one HDR image ... ")
        mergeDebevec = cv2.createMergeDebevec()
        hdrDebevec = mergeDebevec.process(cv_images, exposure_times, crf)
        return hdrDebevec
    except Exception as e:
        print("Merging failed")
        print(e)

    print("Merging complete")