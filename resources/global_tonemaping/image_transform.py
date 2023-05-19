import resources.global_tonemaping as gt
import cv2




def global_image_transformer(BP_images_dict, selector, gamma, saturation, sharpening_itteration, sharpening_s, sharpening_r):
    for exp, img in BP_images_dict.items():
        rgb_image = img.convert("RGB")
        numpy_image = rgb_image.get_numpy_array()

        BP_images_dict[selector][exp] = numpy_image

    result_aligning = gt.HDR_Aligning.aligning(im_dict=BP_images_dict)
    CRF_bottom = gt.HDR_CRF_imp_export.CRF_JSON_importer("./images/configs/crf_bottom.npy")
    result_merging_bottom = gt.HDR_Merging.merging(result_aligning, CRF_bottom, selector=selector)
    result_merging_bottom = cv2.flip(result_merging_bottom, 0)
    result_tonemaping_bottom = gt.HDR_Tonemaping.tonemaping(hdr=result_merging_bottom, selector=selector,
                                              gb=float(gamma),
                                              sb=float(saturation))
    result_sharpening_bottom = gt.LDR_Sharpening.LDR_sharpen(result_tonemaping_bottom, iter=int(sharpening_itteration),
                                              s=int(sharpening_s), r=float(sharpening_r))
    return result_sharpening_bottom