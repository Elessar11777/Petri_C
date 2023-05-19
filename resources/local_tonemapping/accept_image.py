import numpy as np

def image_accepter(BP_images_dict):
    images_b = []
    exposures_b = []
    images_p = []
    exposures_p = []

    for exposure, image in BP_images_dict["Source"]["B"].items():
        images_b.append(image)
        den = 1000
        exposures_b.append(int(exposure/den))
    iter_b = zip(images_b, exposures_b)
    sorted_iter_b = sorted(iter_b, key=lambda pair: pair[1], reverse=True)

    for exposure, image in BP_images_dict["Source"]["P"].items():
        images_p.append(image)
        den = 1000
        exposures_p.append(int(exposure/den))
    iter_p = zip(images_p, exposures_p)
    sorted_iter_p = sorted(iter_p, key=lambda pair: pair[1], reverse=True)

    sorted_dict = {
        "B": {
            [img for img, times in sorted_iter_b]: np.log(sorted(exposures_b, reverse=True))
        },
        "P": {
        [img for img, times in sorted_iter_p]: np.log(sorted(exposures_p, reverse=True))
        }
    }

    return sorted_dict
