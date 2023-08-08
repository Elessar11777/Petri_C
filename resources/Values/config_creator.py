import json

class ConfigCreator:

    def __init__(self, file_path):

        self.hard_values_dict = {}
        self.config_dict = {}

        # Load and clean the JSON data
        with open(file_path, "r", encoding="utf-8") as f:
            self.config_json = json.load(f)
            # Remove keys that start with underscore
            self.clean_data = {key: value for key, value in self.config_json.items() if not key.startswith('_')}
            print(f"Clean data: {self.clean_data}")

    def create_hard_values(self, input_dict):
        output_dict = {}

        for key, value in input_dict.items():
            if isinstance(value, dict):
                if "keys" in value:
                    output_dict[key] = value["keys"]
                else:
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, dict):
                            if "keys" in subvalue:
                                output_dict.setdefault(key, {})[subkey] = subvalue["keys"]
                            else:
                                for subsubkey, subsubvalue in subvalue.items():
                                    if isinstance(subsubvalue, dict) and "keys" in subsubvalue:
                                        output_dict.setdefault(key, {}).setdefault(subkey, {})[subsubkey] = subsubvalue[
                                            "keys"]

        return output_dict

    def create_config_dict(self, input_dict, output_dict=None):
        if output_dict is None:
            output_dict = {}

        excluded_keys = ["param", "values", "keys"]

        if isinstance(input_dict, dict):
            for l1_key, l1_value in input_dict.items():
                if isinstance(l1_value, dict):
                    if "param" in l1_value and "values" in l1_value:
                        if l1_value["param"] is not None and l1_value["values"] is not None:
                            output_dict[l1_value["param"]] = l1_value["values"]
                    for ld_key, ld_value in l1_value.items():
                        if ld_key not in excluded_keys:
                            self.create_config_dict(l1_value, output_dict=output_dict)

        return output_dict
    def dict_to_obj(self, d):
        # Recursively convert a dictionary to a Python object
        if isinstance(d, dict):
            x = type('', (), {})()
            for key, value in d.items():
                if isinstance(value, dict):
                    setattr(x, key, self.dict_to_obj(value))  # Recursively set attributes for nested dictionaries
                else:
                    setattr(x, key, value)
            return x
        else:
            return d

    def process(self):
        # Use the cleaned data to create hard values
        self.hard_values_dict = self.create_hard_values(self.clean_data)
        print(self.hard_values_dict)
        # Convert the result dictionary into an object for easier access
        obj = self.dict_to_obj(self.hard_values_dict)

        return obj

    def process_config(self):
        # Create a configuration dictionary from the cleaned data
        self.config_dict = self.create_config_dict(self.clean_data)
        print(f"Config: {self.config_dict}")
        return self.config_dict

if __name__ == "__main__":
    configurer = ConfigCreator("./config_source.json").process()
else:
    configurer = ConfigCreator("./resources/Values/config_source.json").process()

