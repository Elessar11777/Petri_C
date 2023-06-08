import json
from resources.Values.CodeValues import Parameters
from logger import aeya_logger


def load_parameters_from_file(file_path):
    with open(file_path, 'r') as file:
        parameters_dict = json.load(file)
    return parameters_dict


def save_default_settings():
    parameters_dict = Parameters.get_default_parameters()

    with open('./images/configs/settings.json', 'w') as outfile:
        json.dump(parameters_dict, outfile, indent=4)
    return parameters_dict

def save_settings(settings_dict, settings1, settings2, settings3):
    for key, val in settings_dict.items():
        aeya_logger.info("Values to save:")
        aeya_logger.info(f"{key}: {val.get()}")
    parameters_dict = {
        "exposure_bottom_min": settings_dict["exposure_bottom_min"].get(),
        "exposure_bottom_max": settings_dict["exposure_bottom_max"].get(),
        "exposure_bottom_num": settings_dict["exposure_bottom_num"].get(),
        "exposure_bottom_num_calibration": settings_dict["exposure_bottom_num_calibration"].get(),
        "exposure_perif_min": settings_dict["exposure_perif_min"].get(),
        "exposure_perif_max": settings_dict["exposure_perif_max"].get(),
        "exposure_perif_num": settings_dict["exposure_perif_num"].get(),
        "exposure_perif_num_calibration": settings_dict["exposure_perif_num_calibration"].get(),
        "sharpening_itteration": settings_dict["sharpening_itteration"].get(),
        "sharpening_r": settings_dict["sharpening_r"].get(),
        "sharpening_s": settings_dict["sharpening_s"].get(),
        "gamma_bottom": settings_dict["gamma_bottom"].get(),
        "saturation_bottom": settings_dict["saturation_bottom"].get(),
        "gamma_perif": settings_dict["gamma_perif"].get(),
        "saturation_perif": settings_dict["saturation_perif"].get(),
        "device": settings_dict["device"].get(),
        "tonemapping": settings_dict["tonemapping"].get(),
        "HDR_lambda": settings_dict["HDR_lambda"].get(),
        "HDR_pixels": settings_dict["HDR_pixels"].get(),
        "local_saturation": settings_dict["local_saturation"].get(),
        "local_gamma": settings_dict["local_gamma"].get(),
        "batch_size": settings_dict["batch_size"].get()
    }

    with open('./images/configs/settings.json', 'w') as outfile:
        json.dump(parameters_dict, outfile, indent=4)

    settings1.protocol("WM_DELETE_WINDOW", settings1.withdraw)
    if settings1.state() != "withdrawn":
        settings1.withdraw()
    if settings2.state() != "withdrawn":
        settings2.withdraw()
    if settings3.state() != "withdrawn":
        settings3.withdraw()
