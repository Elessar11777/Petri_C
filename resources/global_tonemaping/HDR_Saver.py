import cv2

from resources.global_tonemaping import HDR_Aligning, HDR_CRF, HDR_Merging


def HDR_saver(hdr, path):
    try:
        #cv2.imwrite(path, hdr)
        cv2.imwrite(path, cv2.cvtColor(hdr, cv2.COLOR_BGR2RGB))
        print(f"Saved HDR in {path}")
    except Exception as e:
        print("Saving failed")
        print(e)