import numpy
import os
from logger import aeya_logger

CRF_B_PATH = "./images/configs/crf_bottom.npy"
CRF_P_PATH = "./images/configs/crf_perif.npy"

PATH_DICT = {
        "B": CRF_B_PATH,
        "P": CRF_P_PATH
    }

def CRF_JSON_exporter(crf_dict):
    if os.path.exists(PATH_DICT["B"]):
        os.remove(PATH_DICT["B"])
    if os.path.exists(PATH_DICT["P"]):
        os.remove(PATH_DICT["P"])


    for light, crf in crf_dict.items():
        with open(PATH_DICT[light], "wb") as f:
            numpy.save(f, crf)
        aeya_logger.info(f"CRF exported in {PATH_DICT[light]}")

def CRF_JSON_importer():
    crf_dict = {
        "B": "",
        "P": ""
    }
    for light, path in PATH_DICT.items():
        with open(path, 'r') as f:
            crf_dict[light] = numpy.load(path, allow_pickle=True)

    aeya_logger.info("CRF is loaded")
    return crf_dict
