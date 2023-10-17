import cv2
import numpy

def tonemaping(hdr, gamma=1.4, saturation=2.0):
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

    tonemapped = cv2.createTonemapDrago(gamma=gamma, saturation=saturation)
    ldrDrago = tonemapped.process(hdr)
    ldrDrago = 3 * ldrDrago
    if numpy.isnan(ldrDrago).any():
        ldrDrago = fill_nan_pixels(ldrDrago)
    ldrDrago = numpy.clip(ldrDrago * 255, 0, 255).astype('uint8')
    invalid_indices = numpy.where((ldrDrago < 0) | (ldrDrago > 255))
    if invalid_indices[0].size > 0:
        print("Found invalid values at the following indices:", invalid_indices)
    else:
        print("No invalid values found.")
    ldrDrago[ldrDrago < 0] = 0
    ldrDrago[ldrDrago > 255] = 255

    return ldrDrago