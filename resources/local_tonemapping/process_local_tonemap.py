from resources.local_tonemapping.acessories.localtonemap import local_tonemap
import cv2


def process_local_tonemap(irradiance_map_dict, saturation=1., gamma=1 / 2.2, numtiles=(24,24)):
    """# tonemap using Opencv's Durand Tonemap algorithm
    tonemap_obj = cv2.createTonemapDurand(gamma=4, sigma_color = 5.0)
    hdr_local = tonemap_obj.process(irmap.astype('float32'))
    mp_plt.figure(figsize=(16,16))
    mp_plt.imshow(hdr_local)"""
    result_dict = {}
    for selector, irradiance_map in irradiance_map_dict.items():
        # compute tonemapped image
        tonemapped_bgr = local_tonemap(irradiance_map, saturation=saturation, gamma_=gamma, numtiles=numtiles)
        # image = tonemapped_bgr[:, :, [2, 1, 0]]
        result_dict[selector] = cv2.flip(tonemapped_bgr, 0)


    return result_dict
