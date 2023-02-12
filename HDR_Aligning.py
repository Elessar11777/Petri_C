import HDR_Test

import cv2

def aligning(cv_images, times):
    """
    Function takes list of opencv images and returns them as list of aligned images
    :param cv_images_in: List of opencv images
    :return: Tuple of list of aligned opencv images and list of exposure times in numpy.ndarray
    """
    if isinstance(cv_images, list):
        pass
    else:
        raise TypeError("Only lists are allowed for 'cv_images'")

    print("Starting aligning images...")

    try:
        alignMTB = cv2.createAlignMTB()
        alignMTB.process(src=cv_images, dst=cv_images)

    except Exception as e:
        print("Images aligning failed")
        print(e)
        return

    print("Aligning is complete")

    return cv_images, times

if __name__ == "__main__":
    images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = aligning(images, times)
    print(result_aligning)
