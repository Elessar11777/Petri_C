import json
from resources.Values.config_creator import ConfigCreator
from logger import aeya_logger


def load_parameters_from_file(file_path):
    with open(file_path, 'r') as file:
        parameters_dict = json.load(file)
    return parameters_dict


def save_default_settings():
    parameters_dict = ConfigCreator("./resources/Values/config_source.json").process_config()

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
        "x_offset": settings_dict["x_offset"].get(),
        "y_offset": settings_dict["y_offset"].get(),

        "device": settings_dict["device"].get(),
        "tonemapping": settings_dict["tonemapping"].get(),
        "HDR_lambda": settings_dict["HDR_lambda"].get(),
        "HDR_pixels": settings_dict["HDR_pixels"].get(),
        "local_saturation": settings_dict["local_saturation"].get(),
        "local_gamma": settings_dict["local_gamma"].get(),
        "batch_size": settings_dict["batch_size"].get(),
        "aeya_server_url": settings_dict["aeya_server_url"].get(),
        "web_server_url": settings_dict["web_server_url"].get(),
        "ml_server_url": settings_dict["ml_server_url"].get(),
        "aeya_server_port": settings_dict["aeya_server_port"].get(),
        "web_server_port": settings_dict["web_server_port"].get(),
        "ml_server_port": settings_dict["ml_server_port"].get(),
        "gmic": settings_dict["gmic"].get(),
        "gmic_check": settings_dict["gmic_check"].get(),
        "root": settings_dict["root"].get(),
        "compression": settings_dict["compression"].get(),
        "gracia_string_rule": settings_dict["gracia_string_rule"].get(),
        "spot_string_rule": settings_dict["spot_string_rule"].get()

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
