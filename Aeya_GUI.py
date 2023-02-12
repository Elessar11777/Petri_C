# -*- coding: utf-8 -*-

import tkinter as tk
import threading
import numpy
from PIL import Image
import cv2
import gxipy as gx
import customtkinter as ct
import json
import webbrowser
import os
from datetime import datetime
import sys

import HDR_Aligning as al
import HDR_Saver as hs
import HDR_CRF
import HDR_Merging as mg
import HDR_Tonemaping as ton
import LDR_Sharpening as sh
import HDR_CRF_imp_export as ie
import LDR_Saver as sv
import Path_handler as ph
import SFTP

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)

class App(ct.CTk):
    def __init__(self):
        super().__init__()

        ###PARAMETERS
        ph.common_path_handler()
        try:
            with open('./images/configs/settings.json', 'r') as infile:
                self.parameters_dict = json.load(infile)
        except:
            self.parameters_dict = None
            if not isinstance(self.parameters_dict, dict):
                self.parameters_dict = {
                    "exposure_bottom_min": 30000,
                    "exposure_bottom_max": 300000,
                    "exposure_bottom_num": 10,
                    "exposure_bottom_num_calibration": 100,
                    "exposure_perif_min": 30000,
                    "exposure_perif_max": 800000,
                    "exposure_perif_num": 10,
                    "exposure_perif_num_calibration": 100,
                    "sharpening_itteration": 2,
                    "sharpening_r": 0.2,
                    "sharpening_s": 20,
                    "gamma_bottom": 1.4,
                    "saturation_bottom": 2.0,
                    "gamma_perif": 2.0,
                    "saturation_perif": 1.2,
                    "device": "Gracia"
                }
                with open('./images/configs/settings.json', 'w') as outfile:
                    json.dump(self.parameters_dict, outfile, indent=4)


        self.exposure_bottom_min = tk.StringVar()
        self.exposure_bottom_min.set(self.parameters_dict["exposure_bottom_min"])

        self.exposure_bottom_max = tk.StringVar()
        self.exposure_bottom_max.set(self.parameters_dict["exposure_bottom_max"])
        self.exposure_bottom_num = tk.StringVar()
        self.exposure_bottom_num.set(self.parameters_dict["exposure_bottom_num"])
        self.exposure_bottom_num_calibration = tk.StringVar()
        self.exposure_bottom_num_calibration.set(self.parameters_dict["exposure_bottom_num_calibration"])
        self.exposure_perif_min = tk.StringVar()
        self.exposure_perif_min.set(self.parameters_dict["exposure_perif_min"])
        self.exposure_perif_max = tk.StringVar()
        self.exposure_perif_max.set(self.parameters_dict["exposure_perif_max"])
        self.exposure_perif_num = tk.StringVar()
        self.exposure_perif_num.set(self.parameters_dict["exposure_perif_num"])
        self.exposure_perif_num_calibration = tk.StringVar()
        self.exposure_perif_num_calibration.set(self.parameters_dict["exposure_perif_num_calibration"])

        self.sharpening_itteration = tk.StringVar()
        self.sharpening_itteration.set(self.parameters_dict["sharpening_itteration"])
        self.sharpening_r = tk.StringVar()
        self.sharpening_r.set(self.parameters_dict["sharpening_r"])
        self.sharpening_s = tk.StringVar()
        self.sharpening_s.set(self.parameters_dict["sharpening_s"])

        self.gamma_bottom = tk.StringVar()
        self.gamma_bottom.set(self.parameters_dict["gamma_bottom"])
        self.saturation_bottom = tk.StringVar()
        self.saturation_bottom.set(self.parameters_dict["saturation_bottom"])
        self.gamma_perif = tk.StringVar()
        self.gamma_perif.set(self.parameters_dict["gamma_perif"])
        self.saturation_perif = tk.StringVar()
        self.saturation_perif.set(self.parameters_dict["saturation_perif"])

        self.device = tk.StringVar()
        self.device.set(self.parameters_dict["device"])

        ###GUI SECTION###
        ct.set_appearance_mode("dark")
        ct.set_default_color_theme("dark-blue")

        self.title("Aeya")
        self.geometry("700x500")
        self.iconbitmap(resource_path("Icon.ico"))

        ###Additional pages
        self.settings = ct.CTkToplevel(self)
        self.settings.iconbitmap(resource_path("Icon.ico"))
        self.settings.withdraw()
        self.settings_2 = ct.CTkToplevel(self)
        self.settings_2.iconbitmap(resource_path("Icon.ico"))
        self.settings_2.withdraw()
        self.settings_3 = ct.CTkToplevel(self)
        self.settings_3.iconbitmap(resource_path("Icon.ico"))
        self.settings_3.withdraw()

        #Device Label
        if self.device.get() == "Spot":
            self.label_device = ct.CTkLabel(self, text="Спот-тест")
        if self.device.get() == "Gracia":
            self.label_device = ct.CTkLabel(self, text="Метод Грация")
        self.label_device.place(relx=0.75, rely=0.09)

        #Device status
        self.device_status_default = "Камера не подключена"
        self.device_status_label = ct.CTkLabel(self, text=self.device_status_default)
        self.device_status_label.place(relx=0.75, rely=0.04)

        #Start stream button
        self.start_text_btn_text = "Начать трансляцию"
        self.start_stream_btn = ct.CTkButton(self, text=self.start_text_btn_text, command=self.start_stream)
        self.start_stream_btn.place(relx=0.02, rely=0.05)


        #Soft trigger button
        self.soft_trigger_btn_text = "Триггер"
        self.soft_trigger_btn = ct.CTkButton(self, text=self.soft_trigger_btn_text, command=self.temp_soft)
        self.soft_trigger_btn.place(relx=0.025, rely=0.9)

        #Folder button
        self.folder_btn_text = "Папка"
        self.folder_btn = ct.CTkButton(self, text=self.folder_btn_text,
                                       command=lambda: webbrowser.open(os.path.realpath("./images/")))
        self.folder_btn.place(relx=0.275, rely=0.9)

        #Settings button
        self.settings_btn_text = "Настройки"
        self.settings_btn = ct.CTkButton(self, text=self.settings_btn_text, command=self.show_settings)
        self.settings_btn.place(relx=0.775, rely=0.9)

        #Sync button
        self.sync_btn_text = "Синхронизация"
        self.sync_btn = ct.CTkButton(self, text=self.sync_btn_text, command=self.show_settings)
        self.sync_btn.place(relx=0.525, rely=0.9)

        #Input configs
        self.PETRI_CODE = tk.StringVar()
        self.PETRI_CODE.trace('w', self.input_change_reaction)

        self.code_label = ct.CTkLabel(self, text="Код:")
        self.code_label.place(relx=0.35, rely=0.05)
        self.input_field = ct.CTkEntry(self, textvariable=self.PETRI_CODE)
        self.input_field.place(relx=0.4, rely=0.05)

        #Input_output_test configs
        #self.output_label = ttk.Label(self, textvariable=self.PETRI_CODE)
        #self.output_label.place(relx=0.35, rely=0.95)

        #Image Frames
        self.frame_0 = ct.CTkFrame(self, fg_color='gray', border_color="black", border_width=5, width=300, height=300)
        self.frame_0.place(x=50, y=120)
        self.frame_1 = ct.CTkFrame(self, fg_color='gray', border_color="black", border_width=5, width=300, height=300)
        self.frame_1.place(x=355, y=120)

        self.image_label_0 = None
        self.image_label_1 = None



        ###CONFIG SECTION###

        self.FLAG = 0
        self.soft_trigger = 0
        self.cam = 0

        self.gamma_lut = None
        self.contrast_lut = None
        self.color_correction_param = None

        self.CRF_bottom = None
        self.CRF_perif = None

        self.device_manager = gx.DeviceManager()
        self.dev_num, self.dev_info_list = self.device_manager.update_device_list()

        if self.dev_num == 0:
            print("Number of enumerated devices is 0")
            self.status_setter("Камера не подключена")
        else:
            print(f"Number of enumerated devices is {self.dev_num}/nCamera is ready")
            self.status_setter("Камера подключена")

            try:
                self.cam = self.device_manager.open_device_by_index(1)
            except Exception as e:  # TODO: need to be loged
                self.status_setter("Не удалось открыть устройство")

        #self.set_parameters()
            ###THREADINGS###
            #self.locker = threading.Lock()




    def save_settings(self):
        self.parameters_dict = {
            "exposure_bottom_min": self.exposure_bottom_min.get(),
            "exposure_bottom_max": self.exposure_bottom_max.get(),
            "exposure_bottom_num": self.exposure_bottom_num.get(),
            "exposure_bottom_num_calibration": self.exposure_bottom_num_calibration.get(),
            "exposure_perif_min": self.exposure_perif_min.get(),
            "exposure_perif_max": self.exposure_perif_max.get(),
            "exposure_perif_num": self.exposure_perif_num.get(),
            "exposure_perif_num_calibration": self.exposure_perif_num_calibration.get(),
            "sharpening_itteration": self.sharpening_itteration.get(),
            "sharpening_r": self.sharpening_r.get(),
            "sharpening_s": self.sharpening_s.get(),
            "gamma_bottom": self.gamma_bottom.get(),
            "saturation_bottom": self.saturation_bottom.get(),
            "gamma_perif": self.gamma_perif.get(),
            "saturation_perif": self.saturation_perif.get(),
            "device": self.device.get()
        }

        with open('./images/configs/settings.json', 'w') as outfile:
            json.dump(self.parameters_dict, outfile, indent=4)

        self.settings.protocol("WM_DELETE_WINDOW", self.settings.withdraw)
        if self.settings.state() != "withdrawn":
            self.settings.withdraw()
        if self.settings_2.state() != "withdrawn":
            self.settings_2.withdraw()
        if self.settings_3.state() != "withdrawn":
            self.settings_3.withdraw()


    ###SETTING PAGES BLOCK

    def show_settings(self):
        self.settings.geometry(self.geometry())

        self.settings.protocol("WM_DELETE_WINDOW", self.settings.withdraw)
        if self.settings_2.state() != "withdrawn":
            self.settings_2.withdraw()
        if self.settings_3.state() != "withdrawn":
            self.settings_3.withdraw()

        self.settings.title("Aeya Настройки")
        self.settings.geometry("700x500")

        save_settings_btn = ct.CTkButton(self.settings, text="Сохранить", command=self.save_settings)
        save_settings_btn.place(relx=0.75, rely=0.9)

        settings_btn_text = "Экспозиция"
        settings_btn = ct.CTkButton(self.settings, text=settings_btn_text, state="disabled")
        settings_btn.place(relx=0.025, rely=0.9)

        settings_btn_text = "Режимы"
        settings_btn = ct.CTkButton(self.settings, text=settings_btn_text, command=self.show_settings_page_3)
        settings_btn.place(relx=0.265, rely=0.9)

        settings_2_btn_text = "Постобработка"
        settings_2_btn = ct.CTkButton(self.settings, text=settings_2_btn_text, command=self.show_settings_page_2)
        settings_2_btn.place(relx=0.5, rely=0.9)

        setting_exposure_bottom_label = ct.CTkLabel(self.settings, text="Экспозиция просвет")
        setting_exposure_bottom_label.place(relx=0.05, rely=0.05)

        setting_exposure_bottom_min_label = ct.CTkLabel(self.settings, text="Минимальная")
        setting_exposure_bottom_min_label.place(relx=0.05, rely=0.13)
        input_exposure_bottom_min = ct.CTkEntry(self.settings, textvariable=self.exposure_bottom_min)
        input_exposure_bottom_min.place(relx=0.4, rely=0.13)

        setting_exposure_bottom_max_label = ct.CTkLabel(self.settings, text="Максимальная")
        setting_exposure_bottom_max_label.place(relx=0.05, rely=0.21)
        input_exposure_bottom_max = ct.CTkEntry(self.settings, textvariable=self.exposure_bottom_max)
        input_exposure_bottom_max.place(relx=0.4, rely=0.21)

        setting_exposure_bottom_num_label = ct.CTkLabel(self.settings, text="Количество")
        setting_exposure_bottom_num_label.place(relx=0.05, rely=0.29)
        input_exposure_bottom_num = ct.CTkEntry(self.settings, textvariable=self.exposure_bottom_num)
        input_exposure_bottom_num.place(relx=0.4, rely=0.29)

        setting_exposure_bottom_num_calibration_label = ct.CTkLabel(self.settings, text="Количество калибровочное")
        setting_exposure_bottom_num_calibration_label.place(relx=0.05, rely=0.37)
        input_exposure_bottom_num_calibration = ct.CTkEntry(self.settings, textvariable=self.exposure_bottom_num_calibration)
        input_exposure_bottom_num_calibration.place(relx=0.4, rely=0.37)

        calibrarion_bottom_btn_text = "Калибровка"
        calibrarion_bottom_btn = ct.CTkButton(self.settings, text=calibrarion_bottom_btn_text,
                                                   command=lambda: self.calibration_thread_B(
                                                    low=int(self.exposure_bottom_min.get()),
                                                    high=int(self.exposure_bottom_max.get()),
                                                    num=int(self.exposure_bottom_num_calibration.get()),
                                                    collection=False
                                        ))
        calibrarion_bottom_btn.place(relx=0.65, rely=0.37)

        setting_exposure_perif_label = ct.CTkLabel(self.settings, text="Экспозиция периферия")
        setting_exposure_perif_label.place(relx=0.05, rely=0.45)


        setting_exposure_perif_min_label = ct.CTkLabel(self.settings, text="Минимальная")
        setting_exposure_perif_min_label.place(relx=0.05, rely=0.53)
        input_exposure_perif_min = ct.CTkEntry(self.settings, textvariable=self.exposure_perif_min)
        input_exposure_perif_min.place(relx=0.4, rely=0.53)

        setting_exposure_perif_max_label = ct.CTkLabel(self.settings, text="Максимальная")
        setting_exposure_perif_max_label.place(relx=0.05, rely=0.61)
        input_exposure_perif_max = ct.CTkEntry(self.settings, textvariable=self.exposure_perif_max)
        input_exposure_perif_max.place(relx=0.4, rely=0.61)

        setting_exposure_perif_num_label = ct.CTkLabel(self.settings, text="Количество")
        setting_exposure_perif_num_label.place(relx=0.05, rely=0.69)
        input_exposure_perif_num = ct.CTkEntry(self.settings, textvariable=self.exposure_perif_num)
        input_exposure_perif_num.place(relx=0.4, rely=0.69)

        setting_exposure_perif_num_calibration_label = ct.CTkLabel(self.settings, text="Количество калибровочное")
        setting_exposure_perif_num_calibration_label.place(relx=0.05, rely=0.77)
        input_exposure_perif_num_calibration = ct.CTkEntry(self.settings, textvariable=self.exposure_perif_num_calibration)
        input_exposure_perif_num_calibration.place(relx=0.4, rely=0.77)

        calibrarion_perif_btn_text = "Калибровка"
        calibrarion_perif_btn = ct.CTkButton(self.settings, text=calibrarion_perif_btn_text,
                                              command=lambda: self.calibration_thread_P(
                                                  low=int(self.exposure_perif_min.get()),
                                                  high=int(self.exposure_perif_max.get()),
                                                  num=int(self.exposure_perif_num_calibration.get()),
                                                  collection=False
                                              ))
        calibrarion_perif_btn.place(relx=0.65, rely=0.77)

        self.settings.deiconify()

    def show_settings_page_2(self):
        self.settings_2.geometry(self.geometry())

        self.settings_2.protocol("WM_DELETE_WINDOW", self.settings_2.withdraw)
        if self.settings.state() != "withdrawn":
            self.settings.withdraw()
        if self.settings_3.state() != "withdrawn":
            self.settings_3.withdraw()

        self.settings_2.title("Aeya Настройки")
        self.settings_2.geometry("700x500")

        setting_postprocessing_label = ct.CTkLabel(self.settings_2, text="Постобработка")
        setting_postprocessing_label.place(relx=0.05, rely=0.05)

        setting_sharpening_itteration_label = ct.CTkLabel(self.settings_2, text="Иттерации резкости")
        setting_sharpening_itteration_label.place(relx=0.05, rely=0.13)
        input_sharpening_itteration = ct.CTkEntry(self.settings_2, textvariable=self.sharpening_itteration)
        input_sharpening_itteration.place(relx=0.4, rely=0.13)

        setting_sharpening_r_label = ct.CTkLabel(self.settings_2, text="R резкости")
        setting_sharpening_r_label.place(relx=0.05, rely=0.21)
        input_sharpening_r = ct.CTkEntry(self.settings_2, textvariable=self.sharpening_r)
        input_sharpening_r.place(relx=0.4, rely=0.21)

        setting_sharpening_s_label = ct.CTkLabel(self.settings_2, text="S резкости")
        setting_sharpening_s_label.place(relx=0.05, rely=0.29)
        input_sharpening_s = ct.CTkEntry(self.settings_2, textvariable=self.sharpening_s)
        input_sharpening_s.place(relx=0.4, rely=0.29)

        setting_toning_bottom_label = ct.CTkLabel(self.settings_2, text="Тонирование просвет")
        setting_toning_bottom_label.place(relx=0.05, rely=0.37)
        input_gamma_bottom = ct.CTkEntry(self.settings_2, textvariable=self.gamma_bottom)
        input_gamma_bottom.place(relx=0.4, rely=0.37)
        input_saturation_bottom = ct.CTkEntry(self.settings_2, textvariable=self.saturation_bottom)
        input_saturation_bottom.place(relx=0.6, rely=0.37)

        setting_toning_perif_label = ct.CTkLabel(self.settings_2, text="Тонирование периферия")
        setting_toning_perif_label.place(relx=0.05, rely=0.45)
        input_gamma_perif = ct.CTkEntry(self.settings_2, textvariable=self.gamma_perif)
        input_gamma_perif.place(relx=0.4, rely=0.45)
        input_saturation_perif = ct.CTkEntry(self.settings_2, textvariable=self.saturation_perif)
        input_saturation_perif.place(relx=0.6, rely=0.45)

        settings_btn_text = "Экспозиция"
        settings_btn = ct.CTkButton(self.settings_2, text=settings_btn_text, command=self.show_settings)
        settings_btn.place(relx=0.025, rely=0.9)

        settings_btn_text = "Режимы"
        settings_btn = ct.CTkButton(self.settings_2, text=settings_btn_text,  command=self.show_settings_page_3)
        settings_btn.place(relx=0.265, rely=0.9)

        settings_2_btn_text = "Постобработка"
        settings_2_btn = ct.CTkButton(self.settings_2, text=settings_2_btn_text, state="disabled")
        settings_2_btn.place(relx=0.5, rely=0.9)

        save_settings_btn = ct.CTkButton(self.settings_2, text="Сохранить", command=self.save_settings)
        save_settings_btn.place(relx=0.75, rely=0.9)

        self.settings_2.deiconify()

    def show_settings_page_3(self):
        self.settings_3.geometry(self.geometry())

        self.settings_3.protocol("WM_DELETE_WINDOW", self.settings_3.withdraw)
        if self.settings_2.state() != "withdrawn":
            self.settings_2.withdraw()
        if self.settings.state() != "withdrawn":
            self.settings.withdraw()

        self.settings_3.title("Aeya Настройки")
        self.settings_3.geometry("700x500")


        segemented_button = ct.CTkSegmentedButton(master=self.settings_3, values=["Метод Грация", "Спот-тест"],
                                                  command=self.device_changer)
        segemented_button.place(relx=0.05, rely=0.05)
        if self.device.get() == "Spot":
            segemented_button.set("Спот-тест")
        if self.device.get() == "Gracia":
            segemented_button.set("Метод Грация")



        settings_btn_text = "Экспозиция"
        settings_btn = ct.CTkButton(self.settings_3, text=settings_btn_text, command=self.show_settings)
        settings_btn.place(relx=0.025, rely=0.9)

        settings_btn_text = "Режимы"
        settings_btn = ct.CTkButton(self.settings_3, text=settings_btn_text, state="disabled")
        settings_btn.place(relx=0.265, rely=0.9)


        settings_2_btn_text = "Постобработка"
        settings_2_btn = ct.CTkButton(self.settings_3, text=settings_2_btn_text, command=self.show_settings_page_2)
        settings_2_btn.place(relx=0.5, rely=0.9)

        save_settings_btn = ct.CTkButton(self.settings_3, text="Сохранить", command=self.save_settings)
        save_settings_btn.place(relx=0.75, rely=0.9)

        self.settings_3.deiconify()



        #Threadings
        self.thread_list = []
        self.thread_count = 0

    ###



    def start_stream(self):
        if self.start_stream_btn.cget("text") == "Начать трансляцию":
            try:
                print("Starting stream...")
                self.cam.stream_on()
                self.FLAG = 1
                self.loop_thread()
            except Exception as e:
                print("Stream starting is failed. Check the camera is connected")
                print(e)

            self.start_stream_btn.configure(text="Прекратить трансляцию")

        else:
            try:
                print("Stopping stream...")
                self.cam.stream_off()
                self.FLAG = 0
            except Exception as e:
                print("Stream stopping is failed. Restart the application")
                print(e)

            self.start_stream_btn.configure(text="Начать трансляцию")


    def device_changer(self, device_to):
        if device_to == "Спот-тест":
            self.device.set("Spot")
            self.label_device.configure(text="Спот-тест")
            print(self.device.get())
        if device_to == "Метод Грация":
            self.device.set("Gracia")
            self.label_device.configure(text="Метод Грация")
            print(self.device.get())


    def image_setter(self, num, numpy_image):
        print(f"Image type is {type(numpy_image)}")
        image = Image.fromarray(numpy_image, 'RGB')
        image_resized = ct.CTkImage(light_image=image,
                                          dark_image=image,
                                          size=(290, 290))
        if num == 0:
            self.label_i_0 = ct.CTkLabel(self.frame_0, text="", width=290, height=290, image=image_resized)
            self.label_i_0.image = image_resized
            self.label_i_0.place(x=5, y=5)
        if num == 1:
            self.label_i_1 = ct.CTkLabel(self.frame_1, text="", width=290, height=290, image=image_resized)
            self.label_i_1.image = image_resized
            self.label_i_1.place(x=5, y=5)


    def status_setter(self, status):
        if status == "Камера не подключена":
            self.device_status_label.configure(text="Камера не подключена")
        elif status == "Камера подключена":
            self.device_status_label.configure(text="Камера подключена")
        elif status == "Не удалось открыть устройство":
            self.device_status_label.configure(text="Не удалось открыть устройство")


    def run_app(self):
        self.mainloop()

    #Threadings
    def loop_thread(self):
        loope = threading.Thread(target=self.loop, daemon=True)
        loope.start()

    def calibration_thread_B(self, low, high, num, collection):
        calib_b = threading.Thread(target=self.b_calibration, args=(low, high,num, collection,), daemon=True)
        calib_b.start()

    def calibration_thread_P(self, low, high, num, collection):
        calib_p = threading.Thread(target=self.p_calibration, args=(low, high,num, collection,), daemon=True)
        calib_p.start()

    def sending_thread(self, local_path, remote_path):
        self.thread_list.append(threading.Thread(target=SFTP.file_sending, args=(local_path, remote_path), daemon=True))
        self.thread_list[self.thread_count].start()
        self.thread_count += 1

    def set_parameters(self):
        self.cam.Width.set(2064)
        self.cam.Height.set(2064)
        if self.device == "Спот-тест":
            self.cam.OffsetX.set(496)
        elif self.device == "Метод Грация":
            self.cam.OffsetX.set(496)
        self.cam.OffsetY.set(0)
        self.cam.PixelFormat.set(gx.GxPixelFormatEntry.BAYER_RG10)
        self.cam.AcquisitionMode.set(gx.GxAcquisitionModeEntry.CONTINUOUS)
        self.cam.ExposureMode.set(gx.GxExposureModeEntry.TIMED)
        self.cam.BalanceWhiteAuto.set(gx.GxAutoEntry.CONTINUOUS)
        self.cam.ExposureAuto.set(gx.GxAutoEntry.OFF)
        #self.cam.AutoExposureTimeMin.set(8)  # us
        #self.cam.AutoExposureTimeMax.set(1000000)  # us

        self.cam.TriggerMode.set(gx.GxSwitchEntry.ON)
        self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.LINE0)

        self.cam.TriggerActivation.set(1)
        self.cam.TriggerFilterRaisingEdge.set(5000)

        self.exposition_bottom = [x for x in range(int(self.exposure_bottom_min.get()), int(self.exposure_bottom_max.get()),
                                                   int((int(self.exposure_bottom_max.get()) - int(self.exposure_bottom_min.get()))
                                                       / int(self.exposure_bottom_num.get())))]
        self.exposure_times_bottom = numpy.array(self.exposition_bottom, dtype=numpy.float32)

        self.exposition_perif = [x for x in range(int(self.exposure_perif_min.get()), int(self.exposure_perif_max.get()),
                                                   int((int(self.exposure_perif_max.get()) - int(self.exposure_perif_min.get()))
                                                       / int(self.exposure_perif_num.get())))]
        self.exposure_times_perif = numpy.array(self.exposition_perif, dtype=numpy.float32)

    def set_parameters_bottom(self):
        self.cam.ExpectedGrayValue.set(250)
        self.cam.AWBLampHouse.set(gx.GxAWBLampHouseEntry.INCANDESCENT)
        self.cam.LUTEnable.set(False)

    def set_parameters_perif(self):
        self.cam.ExpectedGrayValue.set(200)
        self.cam.AWBLampHouse.set(gx.GxAWBLampHouseEntry.D50)
        self.cam.LUTEnable.set(True)
        if self.cam.GammaParam.is_readable():
            self.gamma_lut = None
        else:
            self.gamma_lut = None
        if self.cam.ContrastParam.is_readable():
            self.contrast_value = self.cam.ContrastParam.get()
            self.contrast_lut = gx.Utility.get_contrast_lut(self.contrast_value)
            print(self.contrast_lut)
        else:
            self.contrast_lut = None
        if self.cam.ColorCorrectionParam.is_readable():
            self.color_correction_param = 0
        else:
            self.color_correction_param = 0

    def temp_soft(self):
        self.soft_trigger = 1
        print("Soft trigger pressed")

    def temp_soft_activator(self):
        self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        self.cam.TriggerSoftware.send_command()

    def loop(self):
        print(self.input_field.cget("fg_color"))
        self.set_parameters()

        image_odd = 0
        while self.FLAG == 1:
            if self.soft_trigger == 1:
                self.temp_soft_activator()
            raw_image = self.cam.data_stream[0].get_image()
            if raw_image is None:
                print('Waiting for trigger')
            elif isinstance(raw_image, gx.gxiapi.RawImage):
                self.input_field.configure(state="disable")
                self.input_field.configure(fg_color="green")
                self.input_field.configure(text_color="black")
                print("Triggered")
                if image_odd == 0:
                    self.set_parameters_bottom()
                if image_odd == 1:
                    self.set_parameters_perif()

                # Restart stream to reset cam.data_stream[0].get_image() object to None
                self.cam.stream_off()
                self.cam.stream_on()

                # Set trigger mode to soft to control acquiring inside loop
                self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

                if image_odd == 0:
                    print(f"Expositions is {self.exposition_bottom}")
                    self.image_list_bottom = []
                    for exp in range(len(self.exposition_bottom)):
                        current_exposure = self.exposition_bottom[exp]
                        self.cam.ExposureTime.set(current_exposure)
                        print(f"Exposition time {self.cam.ExposureTime.get()} applied")
                        self.cam.TriggerSoftware.send_command()
                        self.image_list_bottom.append(self.cam.data_stream[0].get_image())
                        print(self.image_list_bottom[exp])
                    print(self.image_list_bottom)
                if image_odd == 1:
                    self.image_list_perif = []
                    for exp in range(len(self.exposition_perif)):
                        current_exposure = self.exposition_perif[exp]
                        self.cam.ExposureTime.set(current_exposure)
                        print(f"Exposition time {self.cam.ExposureTime.get()} applied")
                        self.cam.TriggerSoftware.send_command()
                        self.image_list_perif.append(self.cam.data_stream[0].get_image())
                        print(self.image_list_perif[exp])
                    print(self.image_list_bottom)
                #Return trigger to LINE0
                self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.LINE0)
                # Reset trigger value
                self.cam.stream_off()
                self.cam.stream_on()

                if image_odd == 1:
                    if self.device.get() == "Spot":
                        self.input_field.configure(fg_color="yellow")
                    if self.device.get() == "Gracia":
                        self.input_field.configure(fg_color="yellow")
                    self.image_transform()
                    self.soft_trigger = 0


                if image_odd == 0:
                    image_odd = 1
                else:
                    image_odd = 0
                    self.input_field.configure(state="normal")
                    if self.device.get() == "Spot":
                        self.input_field.configure(fg_color="red")
                        self.PETRI_CODE.set("")

                    if self.device.get() == "Gracia":
                        self.input_field.configure(fg_color="red")

    def input_change_reaction(self, *args):
        self.input_field.configure(fg_color="#343638")
        self.input_field.configure(text_color="white")

    def b_calibration(self, low=10000, high=900000, num=100, collection=False):
        step = int((high - low) / num)
        exposures = [x for x in range(low, high, step)]
        numpy_exposures = numpy.array(exposures, dtype=numpy.float32)

        self.cam.stream_off()
        self.cam.stream_on()

        self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

        image_list = []
        for exp in range(len(exposures)):
            current_exposure = exposures[exp]
            self.cam.ExposureTime.set(current_exposure)
            print(f"Exposition time {self.cam.ExposureTime.get()} applied")
            self.cam.TriggerSoftware.send_command()
            image_list.append(self.cam.data_stream[0].get_image())
            print(image_list[exp])


        for ind, img in enumerate(image_list):
            rgb_image = img.convert("RGB")
            numpy_image = rgb_image.get_numpy_array()

            if collection == True:
                cv2.imwrite(f"CRFs/1/Img_test_{exposures[ind]}.png",
                            cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            image_list[ind] = numpy_image



        result_aligning = al.aligning(cv_images=image_list, times=numpy_exposures)
        CRF = HDR_CRF.CRF_calculate(result_aligning)
        if os.path.exists("./images/configs/crf_bottom.npy"):
            os.remove("./images/configs/crf_bottom.npy")
        ie.CRF_JSON_exporter(CRF, "./images/configs/crf_bottom.npy")

    def p_calibration(self, low=10000, high=900000, num=100, collection=False):
        step = int((high - low) / num)
        exposures = [x for x in range(low, high, step)]
        numpy_exposures = numpy.array(exposures, dtype=numpy.float32)
        self.cam.stream_off()
        self.cam.stream_on()

        self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

        image_list = []
        for exp in range(len(exposures)):
            current_exposure = exposures[exp]
            self.cam.ExposureTime.set(current_exposure)
            print(f"Exposition time {self.cam.ExposureTime.get()} applied")
            self.cam.TriggerSoftware.send_command()
            image_list.append(self.cam.data_stream[0].get_image())
            print(image_list[exp])

        for ind, img in enumerate(image_list):
            rgb_image = img.convert("RGB")
            numpy_image = rgb_image.get_numpy_array()

            if collection == True:
                cv2.imwrite(f"CRFs/1/Img_test_{exposures[ind]}.png",
                            cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            image_list[ind] = numpy_image

        result_aligning = al.aligning(cv_images=image_list, times=numpy_exposures)
        CRF = HDR_CRF.CRF_calculate(result_aligning)
        if os.path.exists("./images/configs/crf_perif.npy"):
            os.remove("./images/configs/crf_perif.npy")
        ie.CRF_JSON_exporter(CRF, "./images/configs/crf_perif.npy")

    def image_transform(self):
        #BOTTOM
        c_time = datetime.now().strftime("%H_%M_%S")
        for ind, img in enumerate(self.image_list_bottom):
            rgb_image = img.convert("RGB")
            numpy_image = rgb_image.get_numpy_array()
            cv2.imwrite(ph.file_path_handler(self.device.get(), "B", exposure=self.exposition_bottom[ind],
                                             source=True, input = self.PETRI_CODE.get(), time=c_time),
                        cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            self.image_list_bottom[ind] = numpy_image
        result_aligning = al.aligning(self.image_list_bottom, self.exposure_times_bottom)

        #if not isinstance(self.CRF_bottom, numpy.ndarray):
        #    try:
        #        print("Trying load bottom CRF from './images/configs/crf_bottom.npy'")
        self.CRF_bottom = ie.CRF_JSON_importer("./images/configs/crf_bottom.npy")
        #    except:
        #        print("Loading bottom CRF failed")
        #        print("We are strongly recommend adjust CRF with calibration tool!")
         #       self.CRF_bottom = HDR_CRF.CRF_calculate(result_aligning)
         #       if os.path.exists("./images/configs/crf_bottom.npy"):
        #            os.remove("./images/configs/crf_bottom.npy")
        #        ie.CRF_JSON_exporter(self.CRF_bottom, "./images/configs/crf_bottom.npy")

        result_merging_bottom = mg.merging(result_aligning, self.CRF_bottom, selector="B")
        result_merging_bottom = cv2.flip(result_merging_bottom, 0)
        hs.HDR_saver(result_merging_bottom, ph.file_path_handler(self.device.get(), "B", format="hdr",
                                             source=True, input = self.PETRI_CODE.get(), time=c_time))

        result_tonemaping_bottom = ton.tonemaping(hdr=result_merging_bottom, selector="B", gb=float(self.gamma_bottom.get()),
                                                  sb=float(self.saturation_bottom.get()))
        result_sharpening_bottom = sh.LDR_sharpen(result_tonemaping_bottom, iter=int(self.sharpening_itteration.get()),
                                                  s=int(self.sharpening_s.get()), r=float(self.sharpening_r.get()))
        self.image_setter(0, result_sharpening_bottom)
        sv.LDR_saver(ldr=result_sharpening_bottom,
                     path=ph.file_path_handler(self.device.get(), "B", input = self.PETRI_CODE.get()))

        ###PERIF
        c_time = datetime.now().strftime("%H_%M_%S")
        for ind, img in enumerate(self.image_list_perif):
            rgb_image = img.convert("RGB")
            numpy_image = rgb_image.get_numpy_array()
            cv2.imwrite(ph.file_path_handler(self.device.get(), "P", exposure=self.exposition_perif[ind],
                                             source=True, input=self.PETRI_CODE.get(), time=c_time),
                        cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            self.image_list_perif[ind] = numpy_image
        result_aligning = al.aligning(self.image_list_perif, self.exposure_times_perif)

        #if not isinstance(self.CRF_perif, numpy.ndarray):
        #    try:
        #        print("Trying load perif CRF from './images/configs/crf_perif.npy'")
        self.CRF_perif = ie.CRF_JSON_importer("./images/configs/crf_perif.npy")
        #    except:
        #        print("Loading perif CRF failed")
        #        print("We are strongly recommend adjust CRF with calibration tool!")
         #       self.CRF_perif = HDR_CRF.CRF_calculate(result_aligning)
         #       if os.path.exists("./images/configs/crf_perif.npy"):
        #            os.remove("./images/configs/crf_perif.npy")
        #        ie.CRF_JSON_exporter(self.CRF_perif, "./images/configs/crf_perif.npy")

        result_merging = mg.merging(result_aligning, self.CRF_perif, selector="P")
        result_merging = cv2.flip(result_merging, 0)
        hs.HDR_saver(result_merging, ph.file_path_handler(self.device.get(), "P", format="hdr",
                                                                 source=True, input=self.PETRI_CODE.get(), time=c_time))
        result_tonemaping = ton.tonemaping(result_merging, selector="P", gp=float(self.gamma_perif.get()),
                                                  sp=float(self.saturation_perif.get()))
        result_sharpening = sh.LDR_sharpen(result_tonemaping, selector="P", iter=int(self.sharpening_itteration.get()),
                                                  s=int(self.sharpening_s.get()), r=float(self.sharpening_r.get()))
        self.image_setter(1, result_sharpening)
        sv.LDR_saver(ldr=result_sharpening,
                     path=ph.file_path_handler(self.device.get(), selector="P", input=self.PETRI_CODE.get()))


if __name__ == "__main__":
   gui = App()
   gui.run_app()