import os
import time
import queue
from logger import aeya_logger
import db_manager
import threading
import requests
import json
from resources.Values import CodeValues
import Settings_processor


class JsonSender():
    def __init__(self):
        aeya_logger.info("Starting sync processor")

        self.queue = queue.Queue()
        self.db = db_manager.DBManager()
        self.db.create_db()
        self.keep_running = True

        self.parameters = Settings_processor.load_parameters_from_file("./images/configs/settings.json")
        print(self.parameters["aeya_server_url"])
        if self.parameters["aeya_server_port"] != "":
            self.url = self.parameters["aeya_server_url"] + ":" + self.parameters["aeya_server_port"]
        else:
            self.url = self.parameters["aeya_server_url"]

        if self.parameters["web_server_port"] != "":
            self.web_url = self.parameters["web_server_url"] + ":" + self.parameters["web_server_port"]
        else:
            self.web_url = self.parameters["web_server_url"]

        if self.parameters["ml_server_port"] != "":
            self.ml_url = self.parameters["ml_server_url"] + ":" + self.parameters["ml_server_port"]
        else:
            self.ml_url = self.parameters["ml_server_url"]
    def run(self):
        aeya_logger.debug("started run")
        try:
            while self.keep_running:
                aeya_logger.debug("run loop")
                time.sleep(5)
                if not self.queue.empty():
                    aeya_logger.debug(f"Printing queue size at run not empty {self.queue.qsize()}")
                    db_row = self.queue.get()
                    print(db_row)
                    index, file_path, status = db_row

                    print(index)
                    print(file_path)
                    print(status)
                    response_code = self.try_sending(file_path)
                    if response_code == 200:
                        self.db.update_status_to_sent(index)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    else:
                        aeya_logger.debug("Sening failed")
                        self.queue.put(db_row)
                else:
                    aeya_logger.debug("Queue empty")
                    for row in self.db.select_unsent():
                        self.queue.put(row)
        except Exception as e:
            print(e)

    def try_sending(self, filename):
        data = self.load_json_from_file(filename)
        if data is None:  # added check for None
            print("data None")
            return

        headers = {'Content-Type': 'application/json'}
        try:
            print("Tying sending")
            print(data["Meta"])
            response = requests.post(f"http://{self.url}/upload/", json=data, headers=headers, timeout=300)
            if response.status_code == 200:
                aeya_logger.info("Success")
                response_json = response.json()
                print(response_json)
                self.short_requester_production(data, response_json)
        except requests.exceptions.RequestException as e:
            aeya_logger.error(f"RequestException: {e}")
        except Exception as e:
            aeya_logger.error(f"Unexpected error: {e}")
        finally:
            return response.status_code

    def load_json_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            aeya_logger.error(f"File {file_path} not found.")
            return None


    # TODO Stricktly need to test
    def short_requester_production(self, original, response, production=False):
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
                "Code": original["Meta"]["Code"],
                # "Dilution": "",
                # "Cell": ""
           },
        }
        if "Dilution" in original["Meta"]:
            short_dict["Meta"]["Dilution"] = original["Meta"]["Dilution"]
        if "Cell" in original["Meta"]:
            short_dict["Meta"]["Cell"] = original["Meta"]["Cell"]

        json_data = json.dumps(short_dict, indent=4)
        print(json_data)

        if production:
            # json_data = json.dumps(short_dict, indent=4)
            headers = {'Content-Type': 'application/json'}
            aeya_logger.info(f"Json to microgen test: {json_data}")
            try:
                response = requests.get(f"http://{self.web_url}", data=json_data, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                aeya_logger.error(f"HTTP error occurred: {err}")
                return
            except Exception as err:
                aeya_logger.error(f"An error occurred: {err}")
                return

            aeya_logger.info(f"Status code: {response.status_code}")
            aeya_logger.info(f"Response content: {response.text}")

if __name__ == "__main__":
    sender = JsonSender()
    sender.run()

