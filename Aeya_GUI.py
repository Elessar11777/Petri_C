# -*- coding: utf-8 -*-

import tkinter as tk
import threading
import numpy
from PIL import Image
import customtkinter as ct
import json
import webbrowser
import os
import sys
import gxipy as gx
import cv2

from multiprocessing import Queue, freeze_support

# Default parameters:
from resources.Values import CodeValues
# Setting processor
import Settings_processor
# Setting widgets
from resources.SecondaryPagesWidgets import SettingsWidgets3, SettingsWidgets2, SettigngWidgets1
# Camera settings
from resources.camera import CameraParameters
# Global tonemap resources
from resources.global_tonemaping import HDR_Aligning as al, HDR_CRF, HDR_CRF_imp_export as ie,\
    Path_handler as ph, image_transform as it
# Local tonemap resources
from resources.local_tonemapping import accept_image, hdr_debevec, irradiance, process_local_tonemap
# Web client resources
from resources.web import client, synchronizer_3
# Mask countouring resources
from resources.contouring import countoring
# Logger
from logger import aeya_logger


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
        aeya_logger.debug("Logger initialized.")
        # Creating all necessary directories if required:
        ph.common_path_handler()

        # Sync parameters
        self.queue = Queue()
        self.status_queue = Queue()
        self.sender = synchronizer_3.JsonSender(self.queue, self.status_queue)
        self.sender.start()

        self.status_var = tk.StringVar()
        self.status_var.set("")
        status_label = ct.CTkLabel(self, textvariable=self.status_var)
        status_label.pack(pady=80)

        # self.update_label()

        # Attempt to load parameters from a settings file. If the file does not exist or is not valid JSON,
        # create a new settings file with default parameters.
        try:
            self.parameters_dict = Settings_processor.load_parameters_from_file(CodeValues.Paths.SETTINGS.value)
            aeya_logger.debug(f"Loaded {CodeValues.Paths.SETTINGS.value}.")
        except (FileNotFoundError, json.JSONDecodeError):
            self.parameters_dict = Settings_processor.save_default_settings()
            aeya_logger.error(f"Saved settings doen't found. Created parameters from default.")
        try:
            # self.parameters = {key: tk.StringVar(value=str(value)) for key, value in self.parameters_dict.items()}
            self.parameters = {key: tk.StringVar() for key, _ in self.parameters_dict.items()}
            for key, value in self.parameters.items():
                aeya_logger.info(f"Parameter to set: {key}: {self.parameters_dict[key]}")
                value.set(self.parameters_dict[key])
            aeya_logger.info("Working parameters dictionary created.")
        except Exception as e:
            aeya_logger.error(f"{e}")
            aeya_logger.error(f"Couldn't create working parameters dictionary. Review sources.")

        self.images_pack = {}

        # ### GUI SECTION ###

        try:
            # Set colormode and theme of tkinter app
            ct.set_appearance_mode(CodeValues.GUI.MODE.value)
            ct.set_default_color_theme(CodeValues.GUI.THEME.value)
            # Set tkinter app title
            self.title(CodeValues.GUI.TITLE.value)
            # Set tkinter app window geometry
            self.geometry(CodeValues.GUI.GEOMETRY.value)
            self.resizable(False, False)

            self.iconbitmap(resource_path(CodeValues.Paths.ICON.value))

            self.label_i_0 = None
            self.label_i_1 = None

            aeya_logger.info("Interface initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")

        # Creates additional pages that could be called by app and withdraw them
        try:
            self.settings = self.create_additional_pages()
            self.settings_2 = self.create_additional_pages()
            self.settings_2_1 = self.create_additional_pages()
            self.settings_3 = self.create_additional_pages()
            aeya_logger.info("Additional pages initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")

        # Configure additional pages
        # Setting 1 window parameters
        try:
            action_list_1 = [lambda: Settings_processor.save_settings(
                                  self.parameters, self.settings, self.settings_2,
                                  self.settings_3),
                             None,
                             self.show_settings_page_3,
                             lambda: self.show_settings_page_2(
                                  mode=self.parameters[CodeValues.ParameterNames.PROCESSING_MODE.value].get()),
                             lambda: self.calibration_thread(
                              b_low=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_MIN.value].get()),
                              b_high=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_MAX.value].get()),
                              b_num=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_NUM_CALIBRATION.value].get()),
                              p_low=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_MIN.value].get()),
                              p_high=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_MAX.value].get()),
                              p_num=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_NUM_CALIBRATION.value].get())
                              ),
                             lambda: self.calibration_thread(
                                 b_low=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_MIN.value].get()),
                                 b_high=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_MAX.value].get()),
                                 b_num=int(self.parameters[
                                               CodeValues.ParameterNames.EXPOSURE_BOTTOM_NUM_CALIBRATION.value].get()),
                                 p_low=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_MIN.value].get()),
                                 p_high=int(self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_MAX.value].get()),
                                 p_num=int(self.parameters[
                                               CodeValues.ParameterNames.EXPOSURE_PERIF_NUM_CALIBRATION.value].get())
                             )
                             ]
            self.widges_dict_settings_1 = self.configure_additional_page(page=self.settings, action_list=action_list_1)
            aeya_logger.debug("Exposure settings pages initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")
        # Setting 2 window parameters
        try:
            action_list_2 = [self.show_settings,
                             self.show_settings_page_3,
                             None,
                             lambda: Settings_processor.save_settings(self.parameters, self.settings,
                                                                      self.settings_2, self.settings_3),
                             ]
            self.widges_dict_settings_2 = self.configure_additional_page(
                               page=self.settings_2,
                               action_list=action_list_2,
                               button_widgets=SettingsWidgets2.button_widgets,
                               label_widgets=SettingsWidgets2.label_widgets_global,
                               entry_widgets=SettingsWidgets2.entry_widgets_global)
            aeya_logger.debug("Global tonemapping settings pages initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")
        # Setting 2_1 window parameters
        try:
            self.widges_dict_settings_2_1 = self.configure_additional_page(page=self.settings_2_1, action_list=action_list_2,
                                           button_widgets=SettingsWidgets2.button_widgets,
                                           label_widgets=SettingsWidgets2.label_widgets_local,
                                           entry_widgets=SettingsWidgets2.entry_widgets_local)
            aeya_logger.debug("Local tonemapping settings pages initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")

        # Setting 3 window parameters
        try:
            self.action_list_3 = [self.show_settings,
                             None,
                             lambda: self.show_settings_page_2(mode="global"),
                             lambda: Settings_processor.save_settings(self.parameters, self.settings,
                                                                      self.settings_2, self.settings_3)
                             ]
            self.widges_dict_settings_3 = self.configure_additional_page(page=self.settings_3,
                                             action_list=self.action_list_3,
                                             segmented_button_action_list=[
                                               self.device_changer,
                                               self.processing_changer
                                             ],
                                             segmented_button_widgets=SettingsWidgets3.segmented_button_widgets,
                                             button_widgets=SettingsWidgets3.button_widgets,
                                             label_widgets=None,
                                             entry_widgets=None)
            aeya_logger.debug("Modes settings pages initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")
        # Initiate device label depending on current settings
        try:
            if self.parameters[CodeValues.ParameterNames.DEVICE.value].get() == CodeValues.Device.SPOT.value:
                self.label_device = ct.CTkLabel(self, text=CodeValues.GUITexts.SPOT.value)
            if self.parameters[CodeValues.ParameterNames.DEVICE.value].get() == CodeValues.Device.GRACIA.value:
                self.label_device = ct.CTkLabel(self, text=CodeValues.GUITexts.GRACIA.value)
            self.label_device.place(relx=0.75, rely=0.09)
            aeya_logger.debug("Device label initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")

        # Initiate camera connection status
        try:
            self.device_status_default = CodeValues.GUITexts.NOT_CONNECTED.value
            self.device_status_label = ct.CTkLabel(self, text=self.device_status_default)
            self.device_status_label.place(relx=0.75, rely=0.04)
            aeya_logger.debug("Connection label initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")
        # Main window buttons
        try:
            # Start stream button
            self.start_stream_btn = self.create_button_widget(
                text_value=CodeValues.GUITexts.START_TRANSLATION_BUTTON.value,
                command=self.start_stream,
                relx=0.025, rely=0.05, parent=self)

            # Soft trigger button
            self.soft_trigger_btn = self.create_button_widget(text_value=CodeValues.GUITexts.TRIGGER_BUTTON.value,
                                                              command=self.temp_soft,
                                                              relx=0.025, rely=0.9, parent=self)

            # Folder button
            self.folder_btn = self.create_button_widget(text_value=CodeValues.GUITexts.FOLDER_BUTTON.value,
                                                        command=lambda: webbrowser.open(os.path.realpath("./images/")),
                                                        relx=0.275, rely=0.9, parent=self)

            # Settings button
            self.folder_btn = self.create_button_widget(text_value=CodeValues.GUITexts.SETTINGS_BUTTON.value,
                                                        command=self.show_settings,
                                                        relx=0.775, rely=0.9, parent=self)

            # Sync button
            self.folder_btn = self.create_button_widget(text_value=CodeValues.GUITexts.SYNC_BUTTON.value,
                                                        command=self.show_settings,
                                                        relx=0.525, rely=0.9, parent=self)
            aeya_logger.debug("Main page buttons initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")
        # Initiate input field
        try:
            self.PETRI_CODE = tk.StringVar()
            self.PETRI_CODE.trace('w', self.input_change_reaction)

            self.code_label = ct.CTkLabel(self, text=CodeValues.GUITexts.CODE_LABEL.value)
            self.code_label.place(relx=0.35, rely=0.05)
            self.input_field = ct.CTkEntry(self, textvariable=self.PETRI_CODE)
            self.input_field.place(relx=0.4, rely=0.05)
            aeya_logger.debug("Input field initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")

        # Initiate image frames widgets
        try:
            self.frame_0 = self.create_frame_widget(self, 50, 120)
            self.frame_1 = self.create_frame_widget(self, 355, 120)

            self.image_label_0 = None
            self.image_label_1 = None

            self.label_i_0 = ct.CTkLabel(self.frame_0, text="", width=290, height=290)
            self.label_i_0.place(x=5, y=5)
            self.label_i_1 = ct.CTkLabel(self.frame_1, text="", width=290, height=290)
            self.label_i_1.place(x=5, y=5)
            aeya_logger.debug("Image frames initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")

        # ###CONFIG SECTION###
        # Flags and identifiers
        self.FLAG = 0
        self.soft_trigger = 0
        self.cam = 0

        # Look-up tables (LUTs) and parameters for image processing
        self.gamma_lut = None
        self.contrast_lut = None
        self.color_correction_param = None

        # Parameters related to Camera Response Function (CRF)
        self.CRF_bottom = None
        self.CRF_perif = None

        # Initiate Gx Device manager
        try:
            self.device_manager = gx.DeviceManager()
            aeya_logger.debug("Camera manager initialized.")
        except Exception as e:
            aeya_logger.error(f"{e}")
        # Check if any cameras is connected
        self.dev_num, self.dev_info_list = self.device_manager.update_device_list()
        if self.dev_num == 0:
            self.status_setter(CodeValues.GUITexts.NOT_CONNECTED.value)
            aeya_logger.debug("Camera not connected. Check connection and reload application.")
        else:
            self.status_setter(CodeValues.GUITexts.CONNECTED.value)
            try:
                self.cam = self.device_manager.open_device_by_index(1)
                aeya_logger.debug("Camera connected.")
            except Exception as e:
                aeya_logger.error(f"{e}")
                self.status_setter(CodeValues.GUITexts.CAMERA_ERROR.value)

        # ###SETTING PAGES BLOCK ###
        self.settings_windows = [self.settings, self.settings_2, self.settings_3]
        for settings_window in self.settings_windows:
            settings_window.protocol("WM_DELETE_WINDOW", settings_window.withdraw)
            if settings_window.state() != "withdrawn":
                settings_window.withdraw()

    # def update_label(self):
    #     try:
    #         status = self.status_queue.get_nowait()
    #         status_str = f"Очередь: {status['queue']}\n{status['uploading']}"
    #         print(status_str)
    #         self.status_var.set(status_str)
    #     except:
    #         pass
    #     self.after(5000, self.update_label)  # Check queue every second


    def create_additional_pages(self):
        try:
            page = ct.CTkToplevel(self)
            page.iconbitmap(resource_path(CodeValues.Paths.ICON.value))
            page.withdraw()
            aeya_logger.debug("Additional page created.")
            return page
        except Exception as e:
            aeya_logger.error(f"{e}")

    def configure_additional_page(self, page, title=CodeValues.GUI.SETTINGS_TITLE.value,
                                  geometry=CodeValues.GUI.GEOMETRY.value,
                                  button_widgets=SettigngWidgets1.button_widgets,
                                  segmented_button_widgets=None,
                                  label_widgets=SettigngWidgets1.label_widgets,
                                  entry_widgets=SettigngWidgets1.entry_widgets,
                                  action_list=[],
                                  segmented_button_action_list=[],
                                  segmented_button_logic=SettingsWidgets3.segmented_button_logic):
        try:
            widgets_dict = {"buttons": [],
                            "labels": [],
                            "entries": [],
                            "segmented_buttons": []
                            }
            page.title(title)
            page.geometry(geometry)
            if button_widgets is not None:
                for i, bw in enumerate(button_widgets, start=0):
                    action = action_list[i]

                    button = self.create_button_widget(text_value=bw[0],
                                              command=action,
                                              relx=bw[1],
                                              rely=bw[2],
                                              parent=page,
                                              state=bw[3])
                    widgets_dict["buttons"].append(button)
            # Create label widgets
            if label_widgets is not None:
                for lw in label_widgets:
                    label = self.create_label_widgets(parent=page,
                                              text=lw[0],
                                              relx=lw[1],
                                              rely=lw[2])
                    widgets_dict["labels"].append(label)

            if entry_widgets is not None:
                for ew in entry_widgets:
                    entry_widget = self.create_entry_widget(page, parameter_key=ew[0])
                    entry_widget.place(relx=ew[1], rely=ew[2])

                    widgets_dict["entries"].append(entry_widget)

            if segmented_button_widgets is not None:
                for i, sbw in enumerate(segmented_button_widgets, start=0):
                    segmented_button_widget = self.create_segmented_button(master=page,
                                                                           values=sbw[0],
                                                                           command=segmented_button_action_list[i],
                                                                           relx=sbw[1],
                                                                           rely=sbw[2])
                    if self.parameters[segmented_button_logic[i][0]].get() == segmented_button_logic[i][1][0]:
                        segmented_button_widget.set(segmented_button_logic[i][1][1])
                    elif self.parameters[segmented_button_logic[i][0]].get() == segmented_button_logic[i][2][0]:
                        segmented_button_widget.set(segmented_button_logic[i][2][1])

                    widgets_dict["segmented_buttons"].append(segmented_button_widget)
            aeya_logger.debug("Additional page configured.")
            return widgets_dict
        except Exception as e:
            aeya_logger.error(e)

    def create_entry_widget(self, master, parameter_key):
        try:
            entry = ct.CTkEntry(master, textvariable=self.parameters[parameter_key])
            aeya_logger.debug("Entry widget created.")
            return entry
        except Exception as e:
            aeya_logger.error(e)

    def create_button_widget(self, text_value, command, relx, rely, parent, state="enabled"):
        try:
            btn_text = text_value
            button = ct.CTkButton(parent, text=btn_text, command=command, state=state)
            button.place(relx=relx, rely=rely)
            aeya_logger.debug("Button widget created.")
            return button
        except Exception as e:
            aeya_logger.error(e)

    def create_segmented_button(self, master, values, command, relx, rely):
        try:
            segmented_button = ct.CTkSegmentedButton(master=master, values=values, command=command)
            segmented_button.place(relx=relx, rely=rely)
            aeya_logger.debug("Segmented button widget created.")
            return segmented_button
        except Exception as e:
            aeya_logger.error(e)

    def create_frame_widget(self, parent, x, y):
        try:
            frame = ct.CTkFrame(parent,
                                fg_color=CodeValues.GUI.IMAGE_FRAME_FOREGROUND.value,
                                border_color=CodeValues.GUI.IMAGE_FRAME_BORDER.value,
                                border_width=CodeValues.GUI.BORDER_WIDTH.value,
                                width=CodeValues.GUI.WIDTH.value,
                                height=CodeValues.GUI.HEIGHT.value)
            frame.place(x=x, y=y)
            aeya_logger.debug("Frame widget created.")
            return frame
        except Exception as e:
            aeya_logger.error(e)

    def create_label_widgets(self, parent, text, relx, rely):
        try:
            label = ct.CTkLabel(parent, text=text)
            label.place(relx=relx, rely=rely)
            aeya_logger.debug("Label widget created.")
            return label
        except Exception as e:
            aeya_logger.error(e)

    def show_settings(self):
        try:
            self.settings.protocol("WM_DELETE_WINDOW", self.settings.withdraw)
            if self.settings_2.state() != "withdrawn":
                self.settings_2.withdraw()
            if self.settings_3.state() != "withdrawn":
                self.settings_3.withdraw()
            self.settings.deiconify()
            aeya_logger.debug("Exposure settings page opened.")
        except Exception as e:
            aeya_logger.error(e)

    def show_settings_page_2(self, mode="global"):
        aeya_logger.debug(f"Finction called with mode {mode}")
        if mode == "global":
            try:
                self.settings_2.protocol("WM_DELETE_WINDOW", self.settings_2.withdraw)
                if self.settings.state() != "withdrawn":
                    self.settings.withdraw()
                if self.settings_3.state() != "withdrawn":
                    self.settings_3.withdraw()
                if self.settings_2_1.state() != "withdrawn":
                    self.settings_2_1.withdraw()
                self.settings_2.deiconify()
                aeya_logger.debug("Global processing settings page opened.")
            except Exception as e:
                aeya_logger.error(e)
        if mode == "local":
            try:
                self.settings_2_1.protocol("WM_DELETE_WINDOW", self.settings_2_1.withdraw)
                if self.settings.state() != "withdrawn":
                    self.settings.withdraw()
                if self.settings_3.state() != "withdrawn":
                    self.settings_3.withdraw()
                if self.settings_2.state() != "withdrawn":
                    self.settings_2.withdraw()
                self.settings_2_1.deiconify()
                aeya_logger.debug("Local processing settings page opened.")
            except Exception as e:
                aeya_logger.error(e)

    def show_settings_page_3(self):
        try:
            self.settings_3.protocol("WM_DELETE_WINDOW", self.settings_3.withdraw)
            if self.settings_2.state() != "withdrawn":
                self.settings_2.withdraw()
            if self.settings.state() != "withdrawn":
                self.settings.withdraw()
            self.settings_3.deiconify()
            aeya_logger.debug("Modes settings page opened.")
        except Exception as e:
            aeya_logger.error(e)

    def start_stream(self):
        if self.start_stream_btn.cget("text") == CodeValues.GUITexts.START_TRANSLATION_BUTTON.value:
            try:
                self.cam.stream_on()
                self.FLAG = 1
                self.loop_thread()
                aeya_logger.info("Stream started.")
            except Exception as e:
                aeya_logger.error("Stream starting is failed. Check the camera is connected")
                aeya_logger.error(e)
            self.start_stream_btn.configure(text=CodeValues.GUITexts.STOP_TRANSLATION_BUTTON.value)
        else:
            try:
                self.cam.stream_off()
                self.FLAG = 0
                aeya_logger.info("Stream stopped.")
            except Exception as e:
                aeya_logger.error("Stream stopping is failed. Restart the application")
                aeya_logger.error(e)
            self.start_stream_btn.configure(text=CodeValues.GUITexts.START_TRANSLATION_BUTTON.value)

    def device_changer(self, device_to):
        try:
            if device_to == CodeValues.GUITexts.SPOT.value:
                self.parameters[CodeValues.ParameterNames.DEVICE.value].set(CodeValues.Device.SPOT.value)
                self.label_device.configure(text=CodeValues.GUITexts.SPOT.value)
                aeya_logger.debug(f"Device set to {CodeValues.Device.SPOT.value}")
            if device_to == CodeValues.GUITexts.GRACIA.value:
                self.parameters[CodeValues.ParameterNames.DEVICE.value].set(CodeValues.Device.GRACIA.value)
                self.label_device.configure(text=CodeValues.GUITexts.GRACIA.value)
                aeya_logger.debug(f"Device set to {CodeValues.Device.GRACIA.value}")
        except Exception as e:
            aeya_logger.error(e)

    def processing_changer(self, processing_to):
        try:
            if processing_to == CodeValues.GUITexts.GLOBAL.value:
                self.parameters[CodeValues.ParameterNames.PROCESSING_MODE.value].set(CodeValues.ProcessingModes.GLOBAL.value)
                self.widges_dict_settings_1["buttons"][3].configure(command=lambda: self.show_settings_page_2(mode="global"))
                self.widges_dict_settings_3["buttons"][2].configure(
                    command=lambda: self.show_settings_page_2(mode="global"))
                aeya_logger.debug(f"Processing mode set to {CodeValues.ProcessingModes.GLOBAL.value}")

            if processing_to == CodeValues.GUITexts.LOCAL.value:
                self.parameters[CodeValues.ParameterNames.PROCESSING_MODE.value].set(CodeValues.ProcessingModes.LOCAL.value)
                self.widges_dict_settings_1["buttons"][3].configure(command=lambda: self.show_settings_page_2(mode="local"))
                self.widges_dict_settings_3["buttons"][2].configure(
                    command=lambda: self.show_settings_page_2(mode="local"))
                aeya_logger.debug(f"Processing mode set to {CodeValues.ProcessingModes.LOCAL.value}")
        except Exception as e:
            aeya_logger.error(e)

    def image_setter(self, selector, image, mask):
        try:
            image = countoring.applying_mask(image, mask)

            image = Image.fromarray(image, 'RGB')
            image_resized = ct.CTkImage(light_image=image,
                                        dark_image=image,
                                        size=(290, 290))
            if selector == CodeValues.Modes.B.value:
                self.label_i_0 = ct.CTkLabel(self.frame_0, text="", width=290, height=290, image=image_resized)
                self.label_i_0.image = image_resized
                self.label_i_0.place(x=5, y=5)
            elif selector == CodeValues.Modes.P.value:
                self.label_i_1 = ct.CTkLabel(self.frame_1, text="", width=290, height=290, image=image_resized)
                self.label_i_1.image = image_resized
                self.label_i_1.place(x=5, y=5)
            aeya_logger.debug(f"New image set in {selector}")
        except Exception as e:
            aeya_logger.error(e)

    def status_setter(self, status):
        try:
            if status == CodeValues.GUITexts.NOT_CONNECTED.value:
                self.device_status_label.configure(text=CodeValues.GUITexts.NOT_CONNECTED.value)
            elif status == CodeValues.GUITexts.CONNECTED.value:
                self.device_status_label.configure(text=CodeValues.GUITexts.CONNECTED.value)
            elif status == CodeValues.GUITexts.CAMERA_ERROR.value:
                self.device_status_label.configure(text=CodeValues.GUITexts.CAMERA_ERROR.value)
            aeya_logger.info(f"Status changed to {status}")
        except Exception as e:
            aeya_logger.error(e)

    def run_app(self):
        try:
            aeya_logger.info("Starting application...")
            self.mainloop()
        except Exception as e:
            aeya_logger.error(e)

    #Threadings
    def loop_thread(self):
        try:
            loope = threading.Thread(target=self.loop, daemon=True)
            loope.start()
        except Exception as e:
            aeya_logger.error(e)

    def calibration_thread(self, b_low, b_high, b_num, p_low, p_high, p_num):
        try:
            calibration = threading.Thread(target=self.global_calibration,
                                           args=(b_low, b_high, b_num, p_low, p_high, p_num),
                                           daemon=True)
            calibration.start()
        except Exception as e:
            aeya_logger.error(e)

    def set_exposures(self):
        try:
            exposure_bottom_min = self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_MIN.value].get()
            exposure_bottom_max = self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_MAX.value].get()
            exposure_bottom_num = self.parameters[CodeValues.ParameterNames.EXPOSURE_BOTTOM_NUM.value].get()

            exposure_perif_min = self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_MIN.value].get()
            exposure_perif_max = self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_MAX.value].get()
            exposure_perif_num = self.parameters[CodeValues.ParameterNames.EXPOSURE_PERIF_NUM.value].get()

            self.exposition_bottom = [x for x in range(int(exposure_bottom_min), int(exposure_bottom_max),
               int((int(exposure_bottom_max) - int(exposure_bottom_min)) / int(exposure_bottom_num)))]
            self.exposure_times_bottom = numpy.array(self.exposition_bottom, dtype=numpy.float32)

            self.exposition_perif = [x for x in range(int(exposure_perif_min), int(exposure_perif_max),
               int((int(exposure_perif_max) - int(exposure_perif_min)) / int(exposure_perif_num)))]
            self.exposure_times_perif = numpy.array(self.exposition_perif, dtype=numpy.float32)
            aeya_logger.info("Exposure for current record session acquired.")
        except Exception as e:
            aeya_logger.error(e)

    def temp_soft(self):
        try:
            self.soft_trigger = 1
            aeya_logger.debug("Soft trigger pressed")
        except Exception as e:
            aeya_logger.error(e)

    def temp_soft_activator(self):
        try:
            self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
            self.cam.TriggerSoftware.send_command()
            aeya_logger.debug("Soft trigger sent")
        except Exception as e:
            aeya_logger.error(e)

    def configure_input_field(self, state, fg_color, text_color=None):
        try:
            self.input_field.configure(state=state, fg_color=fg_color)
            if text_color:
                self.input_field.configure(text_color=text_color)
            aeya_logger.debug(f"Input field configured to state {state}, fg_color {fg_color}, text color {text_color}")
        except Exception as e:
            aeya_logger.error(e)

    def make_photo(self, client, exposure, selector):
        try:
            for exp in exposure:
                self.cam.ExposureTime.set(exp)
                aeya_logger.info(f"Set exposure: {exp}")
                self.cam.TriggerSoftware.send_command()
                image = self.cam.data_stream[0].get_image()
                client.images["Source"][selector][exp] = image
                aeya_logger.info(f"Captured: {exp}")
        except Exception as e:
            aeya_logger.error(e)
    def process_after_photo(self, client, selector):
        for exp, img in client.images["Source"][selector].items():
            rgb_image = img.convert("RGB")
            numpy_image = rgb_image.get_numpy_array()
            client.source_images_filler(image=numpy_image, exposition=exp, light=selector)
    def camera_reset(self):
        try:
            self.cam.stream_off()
            self.cam.stream_on()
            aeya_logger.debug("Camera stream restarted")
        except Exception as e:
            aeya_logger.error(e)

    def loop(self):
        aeya_logger.info("Camera main loop starting...")
        CameraParameters.set_parameters(self.cam)
        self.set_exposures()
        self.http_client = client.HTTPRequester(research=self.parameters[CodeValues.ParameterNames.DEVICE.value].get())
        image_odd = "B"
        while self.FLAG == 1:
            if self.soft_trigger == 1:
                self.temp_soft_activator()
            raw_image = self.cam.data_stream[0].get_image()
            if raw_image is None:
                pass
                # aeya_logger.debug('Waiting for trigger')
            elif isinstance(raw_image, gx.gxiapi.RawImage):

                if image_odd == "B":
                    self.http_client.set_dtime()

                self.configure_input_field(state="disable", fg_color=CodeValues.GUI.GREEN.value,
                                           text_color=CodeValues.GUI.INPUT_TEXT_COLOR.value)
                aeya_logger.info("Triggered")

                # Restart stream to reset cam.data_stream[0].get_image() object to None
                self.camera_reset()

                # Set trigger mode to soft to control acquiring inside loop
                self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

                # Take source photos and append them to client's dictionary
                if image_odd == "B":
                    CameraParameters.set_parameters_bottom(self.cam)
                    self.make_photo(client=self.http_client, exposure=self.exposition_bottom,
                                    selector=CodeValues.Modes.B.value)

                if image_odd == "P":
                    self.gamma_lut, self.contrast_lut, self.color_correction_param = \
                        CameraParameters.set_parameters_perif(self.cam)
                    self.make_photo(client=self.http_client, exposure=self.exposition_perif,
                                    selector=CodeValues.Modes.P.value)

                #Return trigger to LINE0
                self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.LINE0)
                # Reset trigger value
                self.camera_reset()


                if image_odd == "B":
                    image_odd = "P"
                elif image_odd == "P":
                    # Yellow Processing Stage

                    self.configure_input_field(state="disable", fg_color=CodeValues.GUI.YELLOW.value,
                                               text_color=CodeValues.GUI.INPUT_TEXT_COLOR.value)
                    # Initial processing aquired images
                    self.process_after_photo(client=self.http_client, selector=CodeValues.Modes.B.value)
                    self.process_after_photo(client=self.http_client, selector=CodeValues.Modes.P.value)
                    # Secondary transform
                    self.image_transform(client=self.http_client,
                                         mode=self.parameters[CodeValues.ParameterNames.PROCESSING_MODE.value].get())
                    self.soft_trigger = 0

                    # Red End Stage
                    self.configure_input_field(state="normal", fg_color=CodeValues.GUI.RED.value,
                                               text_color=CodeValues.GUI.INPUT_TEXT_COLOR.value)

                    self.http_client.string_interpreter(self.input_field.get())
                    if self.parameters_dict[CodeValues.ParameterNames.DEVICE.value] == CodeValues.Device.SPOT.value:
                        self.PETRI_CODE.set("")

                    self.sender.save_json_locally(self.http_client.requester())
                    self.http_client.reset()

                    image_odd = "B"

    def input_change_reaction(self, *args):
        self.input_field.configure(fg_color="#343638")
        self.input_field.configure(text_color="white")

    def global_calibration(self,
                           b_low=10000, b_high=900000, b_num=100,
                           p_low=10000, p_high=900000, p_num=100):
        aeya_logger.info("Starting global calibration")

        b_step = int((b_high - b_low) / b_num)
        p_step = int((p_high - p_low) / p_num)

        exposures_dict = {
            "B": [x for x in range(b_low, b_high, b_step)],
            "P": [x for x in range(p_low, p_high, p_step)]
        }
        processing_dict = {
            "B": {},
            "P": {}
        }

        for light, exposures_list in exposures_dict.items():
            self.camera_reset()
            self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

            aeya_logger.info(f"Calibration exposure list: {exposures_list}")
            for exposure in exposures_list:
                self.cam.ExposureTime.set(exposure)
                self.cam.TriggerSoftware.send_command()
                processing_dict[light][exposure] = self.cam.data_stream[0].get_image()
                aeya_logger.info(f"Exposition time {self.cam.ExposureTime.get()} applied")
                if isinstance(processing_dict[light][exposure], gx.gxiapi.RawImage):
                    aeya_logger.info("Success")
                else:
                    aeya_logger.error("Failed acquired calibration image.")
        result_dict ={
            "B": {},
            "P": {}
        }

        for light, image_dict in processing_dict.items():
            for exposure, image in image_dict.items():
                result_dict[light][exposure] = image.convert("RGB").get_numpy_array()
        result_aligning = al.aligning(result_dict)

        CRF = HDR_CRF.CRF_calculate(result_aligning)

        ie.CRF_JSON_exporter(CRF)

    def image_transform(self, client, mode):
        aeya_logger.info(f"Call image_transform with mode: {mode}")
        mask = countoring.contour_cutter_circ(BP_images_dict=client.images["Source"])

        if mode == CodeValues.ProcessingModes.GLOBAL.value:
            result = it.global_image_transformer(
                BP_images_dict=client.images["Source"], selector=CodeValues.Modes.B.value,
                gb=self.parameters[CodeValues.ParameterNames.GAMMA_BOTTOM.value].get(),
                sb=self.parameters[CodeValues.ParameterNames.SATURATION_BOTTOM.value].get(),
                gp=self.parameters[CodeValues.ParameterNames.GAMMA_PERIF.value].get(),
                sp=self.parameters[CodeValues.ParameterNames.SATURATION_PERIF.value].get(),
                sharpening_itteration=self.parameters[CodeValues.ParameterNames.SHARPENING_ITTERATION.value].get(),
                sharpening_s=self.parameters[CodeValues.ParameterNames.SHARPENING_S.value].get(),
                sharpening_r=self.parameters[CodeValues.ParameterNames.SHARPENING_R.value].get())

            result["Mask"] = cv2.flip(mask, 0)
            img_for_tk = client.result_image_filler(result, method="global")
            self.image_setter("B", img_for_tk["B"], mask=img_for_tk["Mask"])
            self.image_setter("P", img_for_tk["P"], mask=img_for_tk["Mask"])

        elif mode == CodeValues.ProcessingModes.LOCAL.value:
            exposure_image_dict = accept_image.image_accepter(client.images["Source"])
            channel_dict = hdr_debevec.hdr_debevec(
                exposure_image_dict,
                lambda_=int(self.parameters[CodeValues.ParameterNames.HDR_LAMBDA.value].get()),
                num_px=int(self.parameters[CodeValues.ParameterNames.HDR_PIXELS.value].get()))
            irradiance_map_dict = irradiance.compute_irradiance(channel_dict, exposure_image_dict)
            result_dict = process_local_tonemap.process_local_tonemap(
                irradiance_map_dict,
                saturation=float(self.parameters[CodeValues.ParameterNames.LOCAL_SATURATION.value].get()),
                gamma=float(self.parameters[CodeValues.ParameterNames.LOCAL_GAMMA.value].get()),
                numtiles=tuple([int(self.parameters[CodeValues.ParameterNames.BATCH_SIZE.value].get()),
                                int(self.parameters[CodeValues.ParameterNames.BATCH_SIZE.value].get())]))
            result_dict["Mask"] = cv2.flip(mask, 0)
            img_for_tk = client.result_image_filler(result_dict, method="local")
            self.image_setter("B", img_for_tk["B"], mask=img_for_tk["Mask"])
            self.image_setter("P", img_for_tk["P"], mask=img_for_tk["Mask"])
if __name__ == "__main__":
    # Pyinstaller fix
    freeze_support()
    gui = App()
    gui.run_app()
