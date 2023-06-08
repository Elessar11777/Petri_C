import os
import json
import time
from multiprocessing import Process, Queue, Lock, Manager
from queue import Empty
from threading import Thread
from logger import aeya_logger

import requests


class JsonSender(Process):
    def __init__(self, queue, status_queue):
        super().__init__()
        aeya_logger.info("Starting sync processor")

        self.queue = queue
        self.status_queue = status_queue
        self.status = {'uploading': ""}
        self.status_lock = Lock()  # added lock for status

        self.json_save_path = "./images/dumps/"
        self.deleted_files_path = "./images/deleted/"  # path for deleted files
        self.file_lock = Lock()

        self.keep_running = True

        if not os.path.exists(self.json_save_path):
            os.mkdir(self.json_save_path)
        if not os.path.exists(self.deleted_files_path):  # ensure the deleted files path exists
            os.mkdir(self.deleted_files_path)


    def update_status_loop(self):
        while self.keep_running:
            self.get_status()
            time.sleep(1)

    def get_status(self):
        num_files = len(
            [f for f in os.listdir(self.json_save_path) if f.endswith(".json")])  # count number of json files
        with self.status_lock:
            self.status_queue.put({'queue': num_files})

    def cleanup_deleted_files(self):
        while self.keep_running:
            deleted_files = [f for f in os.listdir(self.deleted_files_path) if f.endswith(".deleted")]
            for file in deleted_files:
                file_path = os.path.join(self.deleted_files_path, file)
                try:
                    with self.file_lock:
                        os.remove(file_path)
                except Exception as e:
                    aeya_logger.error(f"Error while deleting file {file_path}: {e}")
            time.sleep(60)  # sleep for 1 minute before checking again

    def run(self):
        self.update_status_thread = Thread(target=self.update_status_loop)
        self.update_status_thread.start()

        self.cleanup_thread = Thread(target=self.cleanup_deleted_files)
        self.cleanup_thread.start()

        try:
            while self.keep_running:
                time.sleep(5)
                if not self.queue.empty():
                    aeya_logger.debug(f"Printing queue size at run not empty {self.queue.qsize()}")
                    filename = self.queue.get()
                    self.try_sending(filename)
                else:
                    aeya_logger.debug(f"Printing queue size at run else{self.queue.qsize()}")
                    self.load_saved_files_to_queue()
                    aeya_logger.debug(f"Printing queue size after run else {self.queue.qsize()}")
        except KeyboardInterrupt:
            self.keep_running = False
            self.update_status_thread.join()
            self.cleanup_thread.join()

    def try_sending(self, filename):
        data = self.load_json_from_file(filename)
        if data is None:  # added check for None
            return

        headers = {'Content-Type': 'application/json'}
        with self.status_lock:  # added lock
            self.status['uploading'] = "Загрузка"
        try:
            response = requests.post("http://194.186.150.221:1515/upload/", json=data, headers=headers, timeout=300)
            if response.status_code == 200:
                with self.file_lock:
                    os.rename(filename, os.path.join(self.deleted_files_path,
                                                     f"{os.path.basename(filename)}.deleted"))
                aeya_logger.info("Success")
        except requests.exceptions.RequestException as e:
            aeya_logger.error(f"RequestException: {e}")
        except Exception as e:
            aeya_logger.error(f"Unexpected error: {e}")
        finally:  # ensure 'uploading' is reset even if an exception occurs
            with self.status_lock:  # added lock
                self.status['uploading'] = ""

    def load_json_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            aeya_logger.error(f"File {file_path} not found.")
            return None

    def save_json_locally(self, data):
        with self.file_lock:
            if data["Meta"]["Research"] == "gracia":
                filename = os.path.join(self.json_save_path,
                                    f'{data["Meta"]["Date"]}_{data["Meta"]["Time"]}_{data["Meta"]["Bacteria"]}{data["Meta"]["Code"]}-{data["Meta"]["Dilution"]}.json')
            else:
                filename = os.path.join(self.json_save_path,
                                        f'{data["Meta"]["Date"]}_{data["Meta"]["Time"]}_{data["Meta"]["Bacteria"]}{data["Meta"]["Code"]}-{data["Meta"]["Cell"]}.json')
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            aeya_logger.debug(f"Printing queue size after save json locally {self.queue.qsize()}")
            return filename

    def load_saved_files_to_queue(self):
        with self.file_lock:
            for filename in os.listdir(self.json_save_path):
                full_path = os.path.join(self.json_save_path, filename)

                if os.path.exists(full_path) and not filename.endswith(".deleted"):
                    self.queue.put(full_path)
                    aeya_logger.debug(f"Printing queue size after load saved files to queue {self.queue.qsize()}")

