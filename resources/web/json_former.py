import requests
import cv2
import base64
import json
from datetime import datetime, date
import re
import hashlib
import os
import sys
from resources.logger.logger import aeya_logger
import io
from PIL import Image
import copy
import numpy as np

class HTTPRequester:
    def __init__(self, parameters_dict, research="gracia", gmic_request="mirror y -fx_unsharp 1,10,20,2,0,2,1,1,0,0", gmic_check="on",
                 root="/app/filehosting"):

        self.parameters = parameters_dict

        self.research = research.lower()
        self.gmic_request = gmic_request
        self.root = root
        self.gmic_check = gmic_check
        print(os.getcwd())
        with open('./resources/web/json_templates/accepter_template.json') as f:
            self.images_template = json.load(f)

        self.images = copy.deepcopy(self.images_template)

        if self.research == "gracia":
            self.images["Meta"]["Research"] = "gracia"
            self.images["Root"] = "./gracia"
        if self.research == "spot":
            self.images["Meta"]["Research"] = "spot"
            self.images["Root"] = "./spot"

        self.images["Gmic"] = self.gmic_request
        self.images["Root"] = self.root
        self.images["Gmic_check"] = self.gmic_check

    def set_dtime(self):
        self.images["Meta"]["Date"] = date.today().strftime("%d_%m_%Y")
        self.images["Meta"]["Time"] = datetime.now().strftime("%H_%M_%S")
        aeya_logger.debug(f"Meta: {self.images['Meta']}")


    def image_to_base64_and_hash(self, image, image_set, light, exposition=None, compression=2):
        # Source image coming here is RGB
        image = np.flipud(image)
        image_pil = Image.fromarray(image)
        buffer = io.BytesIO()
        print(f"Compression source = {compression}")
        image_pil.save(buffer, format="PNG", compression=9)
        byte_image = buffer.getvalue()
        # byte_image = image.tobytes()
        b64_image = base64.b64encode(byte_image)
        string_image = b64_image.decode('utf-8')

        hash_object = hashlib.sha256(byte_image)
        hash_value = hash_object.hexdigest()

        # This way of source images
        if exposition is not None:
            self.images["Transport_Source"][light][exposition] = string_image
            self.images["Hash"][image_set][light][exposition] = hash_value
            self.images["Source"][light][exposition] = image
            # print(f"{image} added to {self.images['Source'][light][exposition]}")
        #That way of result images
        else:
            self.images[image_set][light] = string_image
            self.images["Hash"][image_set][light] = hash_value

    def source_images_filler(self, image, exposition, light, compression=2):
        print(f"Compression source = {compression}")
        self.image_to_base64_and_hash(image, "Source", light, exposition, compression=compression)

    def result_image_filler(self, images_dict, compression=2):
        result_images = {}
        result_images["Mask"] = images_dict["Mask"]
        for light, image in images_dict.items():
            self.image_to_base64_and_hash(image, "Images", light, compression=compression)
            result_images[light] = image
        return result_images


    def string_interpreter(self, string=''):
        print(string)
        if self.research == "gracia":
            pattern = rf'{self.parameters["gracia_string_rule"].get()}'
            match = re.search(pattern, string)
            print(f"Gracia pattern {pattern}")
            print(f"Gracia match {match}")
            if match:
                self.images["Meta"]["Bacteria"] = match.group(1).lower()
                self.images["Meta"]["Code"] = match.group(2)
                self.images["Meta"]["Clone"] = (match.group(4) if match.group(4) else '')
                self.images["Meta"]["Dilution"] = match.group(5)
        if self.research == "spot":
            pattern = rf'{self.parameters["spot_string_rule"].get()}'
            match = re.search(pattern, string)
            print(f"Spot match {match}")
            if match:
                self.images["Meta"]["Bacteria"] = match.group(1).lower()
                self.images["Meta"]["Code"] = match.group(2)
                self.images["Meta"]["Cell"] = match.group(3)


    def print_dict_structure(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key) + ', size: ' + str(sys.getsizeof(key)) + ' bytes')
            if isinstance(value, dict):
                self.print_dict_structure(value, indent + 1)
            elif isinstance(value, list):
                print('\t' * (indent + 1) + 'List of length: ' + str(len(value)) + ', size: ' + str(
                    sys.getsizeof(value)) + ' bytes')
                for i in value:
                    if isinstance(i, dict):
                        self.print_dict_structure(i, indent + 1)
                    else:
                        print('\t' * (indent + 2) + str(type(i)) + ', size: ' + str(sys.getsizeof(i)) + ' bytes')
            else:
                print('\t' * (indent + 1) + str(type(value)) + ', size: ' + str(sys.getsizeof(value)) + ' bytes')

    def requester(self):
        returning_dict = self.images.copy()
        del returning_dict["Source"]
        print(returning_dict["Gmic"])
        return returning_dict


    def short_requester_production(self, original, response, production=True):
        short_dict = {
            "Links": {
                "B": response["Links"]["B"],
                "P": response["Links"]["P"],
                "Mask": response["Links"]["Mask"]
            },
            "Meta": {
                "Date": original["Meta"]["Date"],
                "Time": original["Meta"]["Time"],
                "Research": original["Meta"]["Research"],
                "Bacteria": original["Meta"]["Bacteria"],
                "Clone": original["Meta"]["Clone"],
                "Code": original["Meta"]["Code"],
                # "Dilution": "",
                # "Cell": ""
           },
        }
        if "Dilution" in original["Meta"]:
            short_dict["Meta"]["Dilution"] = original["Meta"]["Dilution"]
        if "Cell" in original["Meta"]:
            short_dict["Meta"]["Cell"] = original["Meta"]["Cell"]

        if production:
            json_data = json.dumps(short_dict, indent=4)
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.post(self.production_url+"/request/", data=json_data, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                aeya_logger.error(f"HTTP error occurred: {err}")
                return
            except Exception as err:
                aeya_logger.error(f"An error occurred: {err}")
                return

            aeya_logger.info(f"Status code: {response.status_code}")
            aeya_logger.info(f"Response content: {response.text}")

        # with open("i2.json", "w") as j:
        #     json.dump(short_dict, j, indent=4)

    def reset(self):
        self.images = copy.deepcopy(self.images_template)
        if self.research == "gracia":
            self.images["Meta"]["Research"] = "gracia"
            self.images["Root"] = "./gracia"
        if self.research == "spot":
            self.images["Meta"]["Research"] = "spot"
            self.images["Root"] = "./spot"

        self.images["Gmic"] = self.gmic_request
        self.images["Root"] = self.root
        self.images["Gmic_check"] = self.gmic_check
