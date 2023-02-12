import cv2
import numpy as np

import cv2
import numpy as np


def local_tone_mapping(hdr_image, block_size=8):
    # Convert the HDR image to a floating point format
    hdr_image = cv2.imread(hdr_image, cv2.IMREAD_UNCHANGED)
    hdr_image = hdr_image.astype(np.float32)

    # Apply the Gaussian Blur filter to the image
    blur = cv2.GaussianBlur(hdr_image, (block_size, block_size), 0)

    # Compute the scale factor for each pixel
    scale = hdr_image / blur

    # Perform tonemapping on the image
    tonemapped = cv2.linearPolar(scale, (hdr_image.shape[0] // 2, hdr_image.shape[1] // 2), hdr_image.max(),
                                 cv2.WARP_FILL_OUTLIERS)
    tonemapped = np.clip(tonemapped, 0, 1)

    return tonemapped

ldr = local_tone_mapping("./images/img_source/gracia-test/06_02_2023/15_38_39_P_ps1813-1-7/15_38_39_P_ps1813-1-7.hdr", block_size=8)
cv2.imwrite("kek.png", cv2.cvtColor(ldr, cv2.COLOR_RGB2BGR))
#cv2.imshow("Processed Image", ldr)
#cv2.waitKey(0)
#cv2.destroyAllWindows()