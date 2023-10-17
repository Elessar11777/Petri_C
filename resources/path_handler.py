# -*- coding: utf-8 -*-

from datetime import datetime
import os
from resources.Values.CodeValues import Paths
from resources.logger.logger import aeya_logger



def common_path_handler():
    for path in Paths:
        if not os.path.exists(os.path.dirname(path.value)):
            os.makedirs(os.path.dirname(path.value))
            aeya_logger.info(f"Creating {path.value}.")





def file_path_handler(device, selector, time="", exposure="", source=False, input="", format="bmp"):
    current_date = datetime.now().strftime("%d_%m_%Y")
    if time == "":
        current_time = datetime.now().strftime("%H_%M_%S")
    else:
        current_time = time
    if source == False:
        if device == "Spot":
            target_folder = './images/spot-test/'
        if device == "Gracia":
            target_folder = "./images/gracia-test/"
    else:
        if device == "Spot":
            target_folder = './images/img_source/spot-test/'
        if device == "Gracia":
            target_folder = "./images/img_source/gracia-test/"

    if not os.path.exists(f"{target_folder}{current_date}"):
        os.makedirs(f"{target_folder}{current_date}")

    if input != "":
        input = "_" + input

    if exposure != "":
        exposure = "_" + str(exposure)

    if source == False:
        filename = f"{current_time}_{selector}{input}.{format}"
        save_path = f"{target_folder}{os.sep}{current_date}{os.sep}{filename}"
    else:
        if not os.path.exists(f"{target_folder}{os.sep}{current_date}{os.sep}{current_time}_{selector}{input}{os.sep}"):
            os.makedirs(f"{target_folder}{os.sep}{current_date}{os.sep}{current_time}_{selector}{input}{os.sep}")
        save_path = f"{target_folder}{os.sep}{current_date}{os.sep}{current_time}_{selector}{input}{os.sep}" \
                    f"{current_time}_{selector}{input}{exposure}.{format}"

    return save_path