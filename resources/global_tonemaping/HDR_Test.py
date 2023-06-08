import cv2
import numpy as np
import os

from resources.global_tonemaping import HDR_Aligning, HDR_CRF, HDR_CRF_imp_export, HDR_Merging, HDR_Saver, \
HDR_Tonemaping, HDR_Tonemaping, LDR_Saver, Path_handler

def test_cv_images(selector="KP", image_format="bmp", dir="./images/spot-test/27_01_2023/"):
    """
    Function to debug other HDR and opencv functions in Petri project
    :param selector: "KP" for periferal ligh, "IB" for bottom light
    :param image_format: Image format of calibration images, default - bmp
    :return: Tuple of opencv images list and exposure times ndarray
    """
    image_directory = dir
    images = []

    for filename in os.listdir(image_directory):
        if selector in filename:
            images.append(os.path.join(image_directory, filename))

    print(images)

    cv_images = [cv2.imread(image) for image in images]

    exposure_list = []

    for filename in os.listdir(image_directory):
        if selector in filename:
            exp_num = filename.split(f"{selector}.{image_format}")
            exposure_list.append(int(exp_num[0]))

    print(exposure_list)

    exposure_times = np.array(exposure_list, dtype=np.float32)

    return cv_images, exposure_times

"""
try:
    print("Calculating Camera Response Function (CRF) ... ")

    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(cv_images, exposure_times)

    print("Ok")
except Exception as e:
    print("Calculating CRF failed")
    print(e)

# Merge images into an HDR linear image
try:
    print("Merging images into one HDR image ... ")
    mergeDebevec = cv2.createMergeDebevec()
    hdrDebevec = mergeDebevec.process(cv_images, exposure_times, responseDebevec)
    print("Ok")
except Exception as e:
    print("Merging failed")
    print(e)

 # Save HDR image.
try:
  cv2.imwrite("hdrDebevec.hdr", hdrDebevec)
  print("saved hdrDebevec.hdr ")
except Exception as e:
    print("Saving failed")
    print(e)

tonemapped = cv2.createTonemapDrago(gamma=1.2, saturation=1.6)
ldrDrago = tonemapped.process(hdrDebevec)
ldrDrago = 3 * ldrDrago
ldrDrago = np.clip(ldrDrago*255, 0, 255).astype('uint8')

cv2.imwrite("ldrDrago.tiff", ldrDrago)


"""

#Fitting Drago Tonemap
"""
# # Tonemap using Drago's method to obtain 24-bit color image
drago_gamma = []
drago_saturation = []

start_gamma = 0.05
for i in range(60):
    drago_gamma.append(start_gamma)
    start_gamma += 0.05

start_saturation = 0.05
for i in range(60):
    drago_saturation.append(start_saturation)
    start_saturation += 0.05

for gamma in drago_gamma:
    for saturation in drago_saturation:
        tonemapDrago = cv2.createTonemapDrago(gamma, saturation)
        ldrDrago = tonemapDrago.process(hdrDebevec)
        ldrDrago = 3 * ldrDrago
        cv2.imwrite(f"./Drago/ldr-Drago_{gamma}_{saturation}.jpg", ldrDrago * 255)
        print(f"Complete {gamma}_{saturation}")
"""

#Drago Tonemap
"""
try:
  print("Tonemaping using Drago's method ... ")
  tonemapDrago = cv2.createTonemapDrago(0.65, 0.9)
  ldrDrago = tonemapDrago.process(hdrDebevec)
  ldrDrago = 3 * ldrDrago
  cv2.imwrite("ldr-Drago.jpg", ldrDrago * 255)
  print("saved ldr-Drago.jpg")
except:
    print("Drago's tonemaping failed")
"""

#Fitting Reinhard Tonemap
"""
gamma = []
start_gamma = 0.05
for i in range(60):
    gamma.append(start_gamma)
    start_gamma += 0.05

for gam in gamma:
    tonemapReinhard = cv2.createTonemapReinhard(gamma=gam, intensity=0, light_adapt=0, color_adapt=0)
    ldrReinhard = tonemapReinhard.process(hdrDebevec)
    cv2.imwrite(f"./Reinhard/ldr-Reinhard_{gam}.png", ldrReinhard * 255)
    print(f"Complete {gam}")
"""



#Reinhard Tonemap
"""
 # # Tonemap using Reinhard's method to obtain 24-bit color image
try:
  print("Tonemaping using Reinhard's method ... ")
  tonemapReinhard = cv2.createTonemapReinhard(gamma=1.5, intensity=0, light_adapt=0, color_adapt=0)
  ldrReinhard = tonemapReinhard.process(hdrDebevec)
  cv2.imwrite("ldr-Reinhard.png", ldrReinhard * 255)
  print("saved ldr-Reinhard.png")
except:
    print("Reinhard's tonemaping failed")
"""










#Fitting Mantiuk Tonemap






#Mantiuk Tonemap

 # # Tonemap using Mantiuk's method to obtain 24-bit color image
"""
try:
  print("Tonemaping using Mantiuk's method ... ")
  tonemapMantiuk = cv2.createTonemapMantiuk(2.0, 1.10, 2)
  ldrMantiuk = tonemapMantiuk.process(hdrDebevec)
  ldrMantiuk = 3 * ldrMantiuk
  cv2.imwrite("ldr-Mantiuk_2_0__1_10__2_0.jpg", ldrMantiuk * 255)
  print("saved ldr-Mantiuk.jpg")
except:
    print("Mantiuk's tonemaping failed")
"""

