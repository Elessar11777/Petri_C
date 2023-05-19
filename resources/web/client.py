import requests
import cv2
import numpy as np
import base64
import json
from datetime import datetime, date
import re


class HTTPClient:
    def __init__(self, url="", research=""):
        self.url = url
        self.images = {
            "Images": {
                        "B": "image_string",
                        "P": "image_string"
            },
            "Source": {
                "B": {
                    # 1500: "image_string"
                },
                "P": {
                    # 150000: "image_string"
                }
            },
            "Meta": {
                "Date": "",
                "Time": "",
                "Research": "",
                "Bacteria": "",
                "Code": ""
                # "Dilution": "",
                # "Cell": ""

            }
        }
        self.research = research
        if self.research == "gracia":
            self.images["Meta"]["Research"] = "gracia"
        if self.research == "spot":
            self.images["Meta"]["Research"] = "spot"

        self.current_date = date.today().strftime("%d_%m_%Y")
        self.images["Meta"]["Date"] = self.current_date
        self.current_time = datetime.now().strftime("%H_%M_%S")
        self.images["Meta"]["Time"] = self.current_time

    def source_images_filler(self, image, exposition, light):
        byte_image = image.tobytes()
        b64_image = base64.b64encode(byte_image)
        string_image = b64_image.decode('utf-8')
        self.images["Source"][light][exposition] = string_image

    def result_image_filler(self, image, light):
        byte_image = image.tobytes()
        b64_image = base64.b64encode(byte_image)
        string_image = b64_image.decode('utf-8')
        self.images["Images"][light] = string_image
    def string_interpreter(self, string=''):
        if self.research == "gracia":
            pattern = r'^([a-zA-Z]{3})[ _-]?(\d{1,4})[ _-]?(\d{0,2})[ _-](\d{1})$'
            match = re.search(pattern, string)
            if match:
                self.images["Meta"]["Bacteria"] = match.group(1).lower()
                self.images["Meta"]["Code"] = match.group(2) + match.group(3)
                self.images["Meta"]["Dilution"] = match.group(4)
        if self.research == "spot":
            pattern = r'^([a-zA-Z]{3})[ _-]?(\d{1,4})[ _-](\d{1,3})$'
            match = re.search(pattern, string)
            if match:
                self.images["Meta"]["Bacteria"] = match.group(1).lower()
                self.images["Meta"]["Code"] = match.group(2)
                self.images["Meta"]["Cell"] = match.group(3)

    def requester(self):
        json_data = json.dumps(self.images, indent=4)
        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://127.0.0.1:5000/upload', data=json_data, headers=headers)
        print("Status code:", response.status_code)
        print("Response content:", response.text)

if __name__ == '__main__':
    import os


    a = HTTPClient(research="spot")
    a.string_interpreter("Str 1513-1")

    for file in os.listdir("./13_19_10_B_Ac 200-9-6"):
        if file.endswith(".bmp"):
            full_file_path = os.path.join("./13_19_10_B_Ac 200-9-6", file)
            img = cv2.imread(full_file_path)
            _, np_img = cv2.imencode(".png", img, [cv2.IMWRITE_PNG_COMPRESSION, 2])


            pattern = r'_([0-9]{4,})\.bmp$'
            match = re.search(pattern, file)
            exposition = int(match.group(1))

            a.source_images_filler(image=np_img, exposition=exposition, light="B")
    for file in os.listdir("./13_19_15_P_Ac 200-9-6"):
        if file.endswith(".bmp"):
            full_file_path = os.path.join("./13_19_15_P_Ac 200-9-6", file)
            img = cv2.imread(full_file_path)
            _, np_img = cv2.imencode(".png", img, [cv2.IMWRITE_PNG_COMPRESSION, 2])


            pattern = r'_([0-9]{4,})\.bmp$'
            match = re.search(pattern, file)
            exposition = int(match.group(1))

            a.source_images_filler(image=np_img, exposition=exposition, light="P")

    b_img = cv2.imread("B.bmp")
    _, np_img = cv2.imencode(".png", b_img, [cv2.IMWRITE_PNG_COMPRESSION, 2])
    a.result_image_filler(image=np_img, light="B")

    p_img = cv2.imread("P.bmp")
    _, np_img = cv2.imencode(".png", p_img, [cv2.IMWRITE_PNG_COMPRESSION, 2])
    a.result_image_filler(image=np_img, light="P")

    with open('images_spot.json', 'w') as f:
        json.dump(a.images, f, indent=4)

