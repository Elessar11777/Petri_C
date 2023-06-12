import cv2
import numpy
from logger import aeya_logger


# TODO Check how well it is working
def fill_nan_pixels(image):
    # Create a mask of NaNs
    mask = numpy.isnan(image)

    # Loop over all channels and all NaN pixels in each channel
    for c in range(image.shape[2]):
        for y, x in zip(*numpy.where(mask[:, :, c])):
            # Get surrounding pixels
            surrounding = image[max(0, y - 1):min(y + 2, image.shape[0]),
                          max(0, x - 1):min(x + 2, image.shape[1]), c]

            # Avoid considering the NaN pixel itself in the median calculation
            surrounding = surrounding[numpy.isnan(surrounding) == False]

            # Replace the NaN pixel with the median of surrounding pixels
            if surrounding.size:
                image[y, x, c] = numpy.median(surrounding)
            else:
                image[y, x, c] = 0  # or some other value that makes sense in your case

    return image

def tonemaping(hdr_dict, gb=1.4, sb=2.0, gp=1.6, sp=1.6):
    aeya_logger.info("Starting global ldr tonemapping")
    parameters_dict = {
        "B": {
            "gamma": gb,
            "saturation": sb
        },
        "P": {
            "gamma": gp,
            "saturation": sp
        }
    }
    tonemapped_dict = {}
    for light, hdr_image in hdr_dict.items():
        tonemapped = cv2.createTonemapDrago(gamma=parameters_dict[light]["gamma"],
                                            saturation=parameters_dict[light]["saturation"])
        aeya_logger.debug(type(hdr_image))
        aeya_logger.debug(hdr_image)
        ldrDrago = tonemapped.process(hdr_image)
        ldrDrago = 3 * ldrDrago
        # TODO Check source of NaN value pixels
        # If there are any NaN values in the array, fill them in
        if numpy.isnan(ldrDrago).any():
            aeya_logger.error("NaN values found in ldrDrago array, applying NaN fixing method.")
            ldrDrago = fill_nan_pixels(ldrDrago)
        ldrDrago = numpy.clip(ldrDrago * 255, 0, 255).astype('uint8')
        invalid_indices = numpy.where((ldrDrago < 0) | (ldrDrago > 255))
        if invalid_indices[0].size > 0:
            aeya_logger.error("Found invalid values at the following indices:", invalid_indices)
        else:
            aeya_logger.info("No invalid values found.")
        ldrDrago[ldrDrago < 0] = 0
        ldrDrago[ldrDrago > 255] = 255

        tonemapped_dict[light] = ldrDrago

    return tonemapped_dict
