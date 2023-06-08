from resources.global_tonemaping import HDR_Aligning, HDR_CRF_imp_export, HDR_Merging, HDR_Tonemaping, LDR_Sharpening
import cv2
from logger import aeya_logger



def global_image_transformer(BP_images_dict, selector, gb, sb, gp, sp, sharpening_itteration, sharpening_s, sharpening_r):
    aeya_logger.info("Starting global image processing")
    for sel, img_dict in BP_images_dict.items():
        for exp, numpy_image in img_dict.items():

            BP_images_dict[selector][exp] = numpy_image

    result_aligning = HDR_Aligning.aligning(im_dict=BP_images_dict)
    crf_dict = HDR_CRF_imp_export.CRF_JSON_importer()
    result_merging = HDR_Merging.merging(exp_img_dict=result_aligning, crf_dict=crf_dict)

    for light, image in result_merging.items():
        result_merging[light] = cv2.flip(image, 0)

    result_tonemaping = HDR_Tonemaping.tonemaping(hdr_dict=result_merging,
                                                  gb=float(gb),
                                                  sb=float(sb),
                                                  gp=float(gp),
                                                  sp=float(sp))

    result_sharpening = LDR_Sharpening.LDR_sharpen(result_tonemaping, iter=int(sharpening_itteration),
                                                   s=int(sharpening_s), r=float(sharpening_r))

    return result_sharpening
