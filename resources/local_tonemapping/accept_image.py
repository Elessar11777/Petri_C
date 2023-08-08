import numpy as np

def image_accepter(BP_images_dict):
    images_b = []
    exposures_b = []
    images_p = []
    exposures_p = []

    for exposure, image in BP_images_dict["B"].items():
        images_b.append(image)
        den = 1000
        exposures_b.append(int(exposure/den))
    iter_b = zip(images_b, exposures_b)
    sorted_iter_b = sorted(iter_b, key=lambda pair: pair[1], reverse=False)

    for exposure, image in BP_images_dict["P"].items():
        images_p.append(image)
        den = 1000
        exposures_p.append(int(exposure/den))
    iter_p = zip(images_p, exposures_p)
    sorted_iter_p = sorted(iter_p, key=lambda pair: pair[1], reverse=False)

    # Calculate the exposure and image pairs
    B_values = {
        np.log(exposure): img
        for img, exposure in sorted_iter_b
    }

    P_values = {
        np.log(exposure): img
        for img, exposure in sorted_iter_p
    }

    # Then put these pairs into the main dictionary
    sorted_dict = {
        "B": B_values,
        "P": P_values
    }

    return sorted_dict
