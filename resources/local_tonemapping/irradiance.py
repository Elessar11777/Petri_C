import numpy as np
import cv2


def compute_irradiance(channel_dict, exposure_image_dict):
    irradiance_map_dict = {}
    for selector, image_exposure in exposure_image_dict.items():
        crf_channel, _, w = channel_dict[selector]

        image_list = list(image_exposure.values())
        log_exposures = list(image_exposure.keys())

        H, W, C = image_list[0].shape
        num_images = len(image_list)

        # irradiance map for each color channel
        irradiance_map = np.empty((H * W, C))
        for ch in range(C):
            crf = crf_channel[ch]
            num_ = np.empty((num_images, H * W))
            den_ = np.empty((num_images, H * W))
            for j in range(num_images):
                flat_image = (image_list[j][:, :, ch].flatten()).astype('int32')
                num_[j, :] = np.multiply(w[flat_image], crf[flat_image] - log_exposures[j])
                den_[j, :] = w[flat_image]

            irradiance_map[:, ch] = np.sum(num_, axis=0) / (np.sum(den_, axis=0) + 1e-6)

        irradiance_map_dict[selector] = np.reshape(np.exp(irradiance_map), (H, W, C))

    return irradiance_map_dict
