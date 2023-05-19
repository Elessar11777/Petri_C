import HDR_Test

import cv2

def aligning(im_dict):
    """
    Function takes list of opencv images and returns them as list of aligned images
    :param cv_images_in: List of opencv images
    :return: Tuple of list of aligned opencv images and list of exposure times in numpy.ndarray
    """
    if isinstance(cv_images, dict):
        pass
    else:
        raise TypeError("Only lists are allowed for 'cv_images'")
    keys = list(cv_images.keys())
    image_list = list(cv_images.values())
    aligned_images = [None] * len(image_list)

    print("Starting aligning images...")

    try:
        alignMTB = cv2.createAlignMTB()
        alignMTB.process(src=image_list, dst=aligned_images)
        aligned_dict = dict(zip(keys, aligned_images))

    except Exception as e:
        print("Images aligning failed")
        print(e)
        return

    print("Aligning is complete")

    return aligned_dict

if __name__ == "__main__":
    images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = aligning(images, times)
    print(result_aligning)
