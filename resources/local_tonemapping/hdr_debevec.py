import numpy as np
from resources.local_tonemapping.crf import crf_solve
from resources.logger.logger import aeya_logger
import cv2

def hdr_debevec(image_exposure_dict, lambda_=50, num_px=150):
    aeya_logger.info("Start HRD Debevec processing")
    crf_dict = {}
    for selector, image_exposure in image_exposure_dict.items():
        num_images = len(image_exposure)
        Zmin = 0
        Zmax = 255

        images = list(image_exposure.values())
        log_exposures = list(image_exposure.keys())

        # image parameters
        H, W, C = images[0].shape

        # optimization parameters
        px_idx = np.random.choice(H * W, (num_px,), replace=False)

        # define pixel intensity weighting function w
        w = np.concatenate((np.arange(128) - Zmin, Zmax - np.arange(128, 256)))

        # compute Z matrix
        Z = np.empty((num_px, num_images))
        crf_channel = []
        log_irrad_channel = []
        for ch in range(C):
            for j, image in enumerate(images):
                flat_image = image[:, :, ch].flatten()
                Z[:, j] = flat_image[px_idx]

            # get crf and irradiance for each color channel
            [crf, log_irrad] = crf_solve(Z.astype('int32'), log_exposures, lambda_, w, Zmin, Zmax)
            crf_channel.append(crf)
            log_irrad_channel.append(log_irrad)

        crf_dict[selector] = [crf_channel, log_irrad_channel, w]

    return crf_dict
