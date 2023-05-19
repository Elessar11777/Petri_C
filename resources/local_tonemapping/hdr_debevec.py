import numpy as np
from crf import crf_solve

def hdr_debevec(image_exposure_dict, lambda_=50, num_px=150):
    crf_dict = {}
    for selector, image_exposure in image_exposure_dict:
        for images, log_exposures in image_exposure:
            num_images = len(images)
            Zmin = 0
            Zmax = 255

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
