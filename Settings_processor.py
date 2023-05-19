import json
from resources.Values.CodeValues import Parameters


def load_parameters_from_file(file_path):
    with open(file_path, 'r') as file:
        parameters_dict = json.load(file)
    return parameters_dict


def save_settings():
    parameters_dict = Parameters.get_default_parameters()

    with open('./images/configs/settings.json', 'w') as outfile:
        json.dump(parameters_dict, outfile, indent=4)
    return parameters_dict