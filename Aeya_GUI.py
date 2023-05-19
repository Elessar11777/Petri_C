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
import sys

# Default parameters:
from resources.Values import CodeValues
# Setting processor
import Settings_processor
# Setting widgets
from resources.SecondaryPagesWidgets import SettingsWidgets3, SettingsWidgets2, SettigngWidgets1

from resources.camera import CameraParameters

from resources.global_tonemaping import HDR_Aligning as al, HDR_CRF, HDR_CRF_imp_export as ie,\
    Path_handler as ph, image_transform as it
from resources.local_tonemapping import accept_image, hdr_debevec, irradiance, process_local_tonemap
from resources.web import client
from resources.contouring import countoring
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

        # Creating all necessary directories if required:
        ph.common_path_handler()

        # Attempt to load parameters from a settings file. If the file does not exist or is not valid JSON,
        # create a new settings file with default parameters.
        try:
            self.parameters_dict = Settings_processor.load_parameters_from_file(CodeValues.Paths.SETTINGS.value)
        except (FileNotFoundError, json.JSONDecodeError):
            self.parameters_dict = Settings_processor.save_settings()


        self.images_pack = {}

        # ### GUI SECTION ###

        # Set colormode and theme of tkinter app
        ct.set_appearance_mode(CodeValues.GUI.MODE.value)
        ct.set_default_color_theme(CodeValues.GUI.THEME.value)

        # Set tkinter app title
        self.title(CodeValues.GUI.TITLE.value)

        # Set tkinter app window geometry
        self.geometry(CodeValues.GUI.GEOMETRY.value)

        # Set tkinter app icon
        self.iconbitmap(resource_path(CodeValues.Paths.ICON.value))

        # Creates additional pages that could be called by app and withdraw them
        self.settings = ct.CTkToplevel(self)
        self.settings.iconbitmap(resource_path(CodeValues.Paths.ICON.value))
        self.settings.withdraw()
        self.settings_2 = ct.CTkToplevel(self)
        self.settings_2.iconbitmap(resource_path(CodeValues.Paths.ICON.value))
        self.settings_2.withdraw()
        self.settings_3 = ct.CTkToplevel(self)
        self.settings_3.iconbitmap(resource_path(CodeValues.Paths.ICON.value))
        self.settings_3.withdraw()

        # Initiate device label depending on current settings
        if self.device.get() == CodeValues.Device.SPOT.value:
            self.label_device = ct.CTkLabel(self, text=CodeValues.GUITexts.SPOT.value)
        if self.device.get() == CodeValues.Device.GRACIA.value:
            self.label_device = ct.CTkLabel(self, text=CodeValues.Device.GRACIA.value)
        self.label_device.place(relx=0.75, rely=0.09)

        # Initiate camera connection status
        self.device_status_default = CodeValues.GUITexts.NOT_CONNECTED.value
        self.device_status_label = ct.CTkLabel(self, text=self.device_status_default)
        self.device_status_label.place(relx=0.75, rely=0.04)

        # Start stream button
        self.start_stream_btn = self.create_button_widget(text_value=CodeValues.GUITexts.START_TRANSLATION_BUTTON.value,
                                                          command=self.start_stream,
                                                          relx=0.02, rely=0.05, parent=self)

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

        # Initiate input field
        self.PETRI_CODE = tk.StringVar()
        self.PETRI_CODE.trace('w', self.input_change_reaction)

        self.code_label = ct.CTkLabel(self, text=CodeValues.GUITexts.CODE_LABEL.value)
        self.code_label.place(relx=0.35, rely=0.05)
        self.input_field = ct.CTkEntry(self, textvariable=self.PETRI_CODE)
        self.input_field.place(relx=0.4, rely=0.05)

        # Initiate image frames widgets
        self.frame_0 = self.create_frame_widget(self, 50, 120)
        self.frame_1 = self.create_frame_widget(self, 355, 120)

        self.image_label_0 = None
        self.image_label_1 = None

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
        self.device_manager = gx.DeviceManager()

        # Check if any cameras is connected
        self.dev_num, self.dev_info_list = self.device_manager.update_device_list()
        if self.dev_num == 0:
            print("Number of enumerated devices is 0")
            self.status_setter(CodeValues.GUITexts.NOT_CONNECTED.value)
        else:
            print(f"Number of enumerated devices is {self.dev_num}/nCamera is ready")
            self.status_setter(CodeValues.GUITexts.CONNECTED.value)
            try:
                self.cam = self.device_manager.open_device_by_index(1)
            except Exception as e:  # TODO: need to be loged
                self.status_setter(CodeValues.GUITexts.CAMERA_ERROR.value)

        # ###SETTING PAGES BLOCK ###
        self.settings_windows = [self.settings, self.settings_2, self.settings_3]
        for settings_window in self.settings_windows:
            settings_window.protocol("WM_DELETE_WINDOW", settings_window.withdraw)
            if settings_window.state() != "withdrawn":
                settings_window.withdraw()

    def create_entry_widget(self, master, parameter_key):
        string_var = tk.StringVar()
        string_var.set(self.parameters_dict[parameter_key])
        entry = ct.CTkEntry(master, textvariable=string_var)
        return entry

    def create_button_widget(self, text_value, command, relx, rely, parent, state="enabled"):
        btn_text = text_value.value
        button = ct.CTkButton(parent, text=btn_text, command=command, state=state)
        button.place(relx=relx, rely=rely)
        return button

    def create_segmented_button(self, master, values, command, relx, rely):
        segmented_button = ct.CTkSegmentedButton(master=master, values=values, command=command)
        segmented_button.place(relx=relx, rely=rely)
        return segmented_button

    def create_frame_widget(self, parent, x, y):
        frame = ct.CTkFrame(parent,
                            fg_color=CodeValues.GUI.IMAGE_FRAME_FOREGROUND.value,
                            border_color=CodeValues.GUI.IMAGE_FRAME_BORDER.value,
                            border_width=CodeValues.GUI.BORDER_WIDTH.value,
                            width=CodeValues.GUI.WIDTH.value,
                            height=CodeValues.GUI.HEIGHT.value)
        frame.place(x=x, y=y)
        return frame

    def create_label_widgets(self, parent, text, relx, rely):
        label = ct.CTkLabel(parent, text=text)
        label.place(relx=relx, rely=rely)
        return label

    def show_settings(self):
        self.settings.protocol("WM_DELETE_WINDOW", self.settings.withdraw)
        if self.settings_2.state() != "withdrawn":
            self.settings_2.withdraw()
        if self.settings_3.state() != "withdrawn":
            self.settings_3.withdraw()

        # Setting window parameters
        self.settings.title(CodeValues.GUI.SETTINGS_TITLE.value)
        self.settings.geometry(CodeValues.GUI.GEOMETRY.value)

        for bw in SettigngWidgets1.button_widgets:
            action = None
            if bw[0] == SettigngWidgets1.ButtonActions.SETTINGS_SAVE_BUTTON:
                action = self.save_settings
            elif bw[0] == SettigngWidgets1.ButtonActions.EXPOSURE_BOTTOM:
                continue
            elif bw[0] == SettigngWidgets1.ButtonActions.MODES_BUTTON:
                action = self.show_settings_page_3
            elif bw[0] == SettigngWidgets1.ButtonActions.POSTPROCESSING_BUTTON:
                action = self.show_settings_page_2
            elif bw[0] == SettigngWidgets1.ButtonActions.CALIBRATION_BUTTON_B:
                def action_b():
                    return self.calibration_thread_B(
                        low=int(self.exposure_bottom_min.get()),
                        high=int(self.exposure_bottom_max.get()),
                        num=int(self.exposure_bottom_num_calibration.get()),
                        collection=False)
                action = action_b
            elif bw[0] == SettigngWidgets1.ButtonActions.CALIBRATION_BUTTON_P:
                def action_p():
                    return self.calibration_thread_P(
                        low=int(self.exposure_perif_min.get()),
                        high=int(self.exposure_perif_max.get()),
                        num=int(self.exposure_perif_num_calibration.get()),
                        collection=False)
                action = action_p

            self.create_button_widget(text_value=bw[0].name,
                                      command=action,
                                      relx=bw[1],
                                      rely=bw[2],
                                      parent=self.settings,
                                      state=bw[3])

            # Create label widgets
            for lw in SettigngWidgets1.label_widgets:
                self.create_label_widgets(parent=self.settings,
                                          text=lw[0],
                                          relx=lw[1],
                                          rely=lw[2])

            for ew in SettigngWidgets1.entry_widgets:
                entry_widget = self.create_entry_widget(self.settings, parameter_key=ew[0])
                entry_widget.place(relx=ew[1], rely=ew[2])

        self.settings.deiconify()

    def show_settings_page_2(self):
        self.settings_2.geometry(self.geometry())

        self.settings_2.protocol("WM_DELETE_WINDOW", self.settings_2.withdraw)
        if self.settings.state() != "withdrawn":
            self.settings.withdraw()
        if self.settings_3.state() != "withdrawn":
            self.settings_3.withdraw()

        self.settings_2.title(CodeValues.GUI.SETTINGS_TITLE.value)
        self.settings_2.geometry(CodeValues.GUI.GEOMETRY.value)

        # Create button widgets
        for bw in SettingsWidgets2.button_widgets:
            action = None
            if bw[0] == SettingsWidgets2.ButtonActions.SETTINGS_SAVE_BUTTON:
                action = self.save_settings
            elif bw[0] == SettingsWidgets2.ButtonActions.EXPOSURE_BUTTON:
                action = self.show_settings  # Adjust to your method name
            elif bw[0] == SettingsWidgets2.ButtonActions.MODES_BUTTON:
                action = self.show_settings_page_3
            elif bw[0] == SettingsWidgets2.ButtonActions.POSTPROCESSING_BUTTON:
                action = None  # Disable action since button is disabled
            # Add your other conditions here...
            self.create_button_widget(text_value=CodeValues.GUITexts[bw[0].name],
                                      command=action,
                                      relx=bw[1],
                                      rely=bw[2],
                                      parent=self.settings_2,
                                      state=bw[3])

        # Create label widgets
        for lw in SettingsWidgets2.label_widgets:
            self.create_label_widgets(parent=self.settings_2, text=lw[0], relx=lw[1], rely=lw[2])

        # Create entry widgets
        for ew in SettingsWidgets2.entry_widgets:
            entry_widget = self.create_entry_widget(master=self.settings_2, parameter_key=ew[0])
            entry_widget.place(relx=ew[1], rely=ew[2])

        self.settings_2.deiconify()

    def show_settings_page_3(self):
        self.settings_3.geometry(self.geometry())

        self.settings_3.protocol("WM_DELETE_WINDOW", self.settings_3.withdraw)
        if self.settings_2.state() != "withdrawn":
            self.settings_2.withdraw()
        if self.settings.state() != "withdrawn":
            self.settings.withdraw()

        self.settings_3.title(CodeValues.GUI.SETTINGS_TITLE.value)
        self.settings_3.geometry(CodeValues.GUI.GEOMETRY.value)

        segemented_button = self.create_segmented_button(
            master=self.settings_3,
             values=[CodeValues.GUITexts.GRACIA.value, CodeValues.GUITexts.SPOT.value],
             command=self.device_changer,
             relx=0.05, rely=0.05)

        if self.device.get() == CodeValues.Device.SPOT.value:
            segemented_button.set(CodeValues.GUITexts.SPOT.value)
        if self.device.get() == CodeValues.Device.GRACIA.value:
            segemented_button.set(CodeValues.GUITexts.GRACIA.value)

        # Create button widgets
        for bw in SettingsWidgets3.button_widgets:
            action = None
            if bw[0] == SettingsWidgets3.ButtonActions.SETTINGS_SAVE_BUTTON:
                action = self.save_settings
            elif bw[0] == SettingsWidgets3.ButtonActions.EXPOSURE_BUTTON:
                action = self.show_settings  # Adjust to your method name
            elif bw[0] == SettingsWidgets3.ButtonActions.MODES_BUTTON:
                pass
            elif bw[0] == SettingsWidgets2.ButtonActions.POSTPROCESSING_BUTTON:
                action = self.show_settings_page_2


            self.create_button_widget(text_value=CodeValues.GUITexts[bw[0].name],
                                      command=action,
                                      relx=bw[1],
                                      rely=bw[2],
                                      parent=self.settings_2,
                                      state=bw[3])

        self.settings_3.deiconify()

    def start_stream(self):
        if self.start_stream_btn.cget("text") == CodeValues.GUITexts.START_TRANSLATION_BUTTON.value:
            try:
                print("Starting stream...")
                self.cam.stream_on()
                self.FLAG = 1
                self.loop_thread()
            except Exception as e:
                print("Stream starting is failed. Check the camera is connected")
                print(e)

            self.start_stream_btn.configure(text=CodeValues.GUITexts.STOP_TRANSLATION_BUTTON.value)

        else:
            try:
                print("Stopping stream...")
                self.cam.stream_off()
                self.FLAG = 0
            except Exception as e:
                print("Stream stopping is failed. Restart the application")
                print(e)

            self.start_stream_btn.configure(text=CodeValues.GUITexts.START_TRANSLATION_BUTTON.value)

    def device_changer(self, device_to):
        if device_to == CodeValues.GUITexts.SPOT.value:
            self.device.set(CodeValues.Device.SPOT.value)
            self.label_device.configure(text=CodeValues.GUITexts.SPOT.value)
            print(self.device.get())
        if device_to == CodeValues.GUITexts.GRACIA.value:
            self.device.set(CodeValues.Device.GRACIA.value)
            self.label_device.configure(text=CodeValues.GUITexts.GRACIA.value)
            print(self.device.get())

    def image_setter(self, selector, numpy_image):
        print(f"Image type is {type(numpy_image)}")
        image = Image.fromarray(numpy_image, 'RGB')
        image_resized = ct.CTkImage(light_image=image,
                                          dark_image=image,
                                          size=(290, 290))
        if selector == CodeValues.Modes.B.value:
            self.label_i_0 = ct.CTkLabel(self.frame_0, text="", width=290, height=290, image=image_resized)
            self.label_i_0.image = image_resized
            self.label_i_0.place(x=5, y=5)
        if selector == CodeValues.Modes.P.value:
            self.label_i_1 = ct.CTkLabel(self.frame_1, text="", width=290, height=290, image=image_resized)
            self.label_i_1.image = image_resized
            self.label_i_1.place(x=5, y=5)

    def status_setter(self, status):
        if status == CodeValues.GUITexts.NOT_CONNECTED.value:
            self.device_status_label.configure(text=CodeValues.GUITexts.NOT_CONNECTED.value)
        elif status == CodeValues.GUITexts.CONNECTED.value:
            self.device_status_label.configure(text=CodeValues.GUITexts.CONNECTED.value)
        elif status == CodeValues.GUITexts.CAMERA_ERROR.value:
            self.device_status_label.configure(text=CodeValues.GUITexts.CAMERA_ERROR.value)

    def run_app(self):
        self.mainloop()

    #Threadings
    def loop_thread(self):
        loope = threading.Thread(target=self.loop, daemon=True)
        loope.start()

    def calibration_thread_B(self, low, high, num, collection):
        calib_b = threading.Thread(target=self.b_calibration, args=(low, high, num, collection,), daemon=True)
        calib_b.start()

    def calibration_thread_P(self, low, high, num, collection):
        calib_p = threading.Thread(target=self.p_calibration, args=(low, high, num, collection,), daemon=True)
        calib_p.start()

    def sending_thread(self, local_path, remote_path):
        self.thread_list.append(threading.Thread(target=SFTP.file_sending, args=(local_path, remote_path), daemon=True))
        self.thread_list[self.thread_count].start()
        self.thread_count += 1

    def set_exposures(self):
        self.exposition_bottom = [x for x in range(int(self.exposure_bottom_min.get()), int(self.exposure_bottom_max.get()),
                                                   int((int(self.exposure_bottom_max.get()) - int(self.exposure_bottom_min.get()))
                                                       / int(self.exposure_bottom_num.get())))]
        self.exposure_times_bottom = numpy.array(self.exposition_bottom, dtype=numpy.float32)

        self.exposition_perif = [x for x in range(int(self.exposure_perif_min.get()), int(self.exposure_perif_max.get()),
                                                   int((int(self.exposure_perif_max.get()) - int(self.exposure_perif_min.get()))
                                                       / int(self.exposure_perif_num.get())))]
        self.exposure_times_perif = numpy.array(self.exposition_perif, dtype=numpy.float32)

    def temp_soft(self):
        self.soft_trigger = 1
        print("Soft trigger pressed")

    def temp_soft_activator(self):
        self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        self.cam.TriggerSoftware.send_command()

    def loop(self):
        CameraParameters.set_parameters(self.cam)
        self.set_exposures()

        image_odd = 0
        while self.FLAG == 1:
            if self.soft_trigger == 1:
                self.temp_soft_activator()
            raw_image = self.cam.data_stream[0].get_image()
            if raw_image is None:
                print('Waiting for trigger')
            elif isinstance(raw_image, gx.gxiapi.RawImage):
                http_client = client.HTTPClient()



                self.input_field.configure(state="disable")
                self.input_field.configure(fg_color=CodeValues.GUI.GREEN.value)
                self.input_field.configure(text_color=CodeValues.GUI.INPUT_TEXT_COLOR.value)
                print("Triggered")
                if image_odd == 0:
                    CameraParameters.set_parameters_bottom(self.cam)
                if image_odd == 1:
                    self.gamma_lut, self.contrast_lut, self.color_correction_param = \
                        CameraParameters.set_parameters_perif(self.cam)

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
                        # self.image_list_bottom.append(self.cam.data_stream[0].get_image())
                        http_client.images["Source"][
                            CodeValues.Modes.B.value][current_exposure] = self.cam.data_stream[0].get_image()
                        print(self.image_list_bottom[exp])
                    print(self.image_list_bottom)
                if image_odd == 1:
                    self.image_list_perif = []
                    for exp in range(len(self.exposition_perif)):
                        current_exposure = self.exposition_perif[exp]
                        self.cam.ExposureTime.set(current_exposure)
                        print(f"Exposition time {self.cam.ExposureTime.get()} applied")
                        self.cam.TriggerSoftware.send_command()
                        # self.image_list_perif.append(self.cam.data_stream[0].get_image())
                        http_client.images["Source"][
                            CodeValues.Modes.P.value][current_exposure] = self.cam.data_stream[0].get_image()
                        print(self.image_list_perif[exp])
                    print(self.image_list_bottom)
                #Return trigger to LINE0
                self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.LINE0)
                # Reset trigger value
                self.cam.stream_off()
                self.cam.stream_on()

                if image_odd == 1:
                    if self.device.get() == CodeValues.Device.SPOT.value:
                        self.input_field.configure(fg_color=CodeValues.GUI.YELLOW.value)
                    if self.device.get() == CodeValues.Device.SPOT.value:
                        self.input_field.configure(fg_color=CodeValues.GUI.YELLOW.value)
                    self.image_transform(image_pack=http_client.images, mode="global")
                    self.soft_trigger = 0

                if image_odd == 0:
                    image_odd = 1
                else:
                    image_odd = 0
                    self.input_field.configure(state="normal")
                    if self.device.get() == CodeValues.Device.SPOT.value:
                        self.input_field.configure(fg_color="red")
                        self.PETRI_CODE.set("")

                    if self.device.get() == CodeValues.Device.GRACIA.value:
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

    def image_transform(self, image_pack, mode):
        mask = countoring.contour_cutter_circ(BP_images_dict=image_pack)
        image_pack = countoring.applying_mask(BP_images_dict=image_pack, mask=mask)

        if mode == CodeValues.ProcessingModes.GLOBAL:
            # BOTTOM
            result_B = it.global_image_transformer(BP_images_dict=image_pack, selector=CodeValues.Modes.B.value,
                                                   gamma=self.gamma_bottom.get(),
                                                   saturation=self.saturation_bottom.get(),
                                                   sharpening_itteration=self.sharpening_itteration.get(),
                                                   sharpening_s=self.sharpening_s.get(),
                                                   sharpening_r=self.sharpening_r.get())
            image_pack["Image"][CodeValues.Modes.B.value] = result_B
            # PERIF
            result_P = it.global_image_transformer(BP_images_dict=image_pack, selector=CodeValues.Modes.P.value,
                                                   gamma=self.gamma_perif.get(),
                                                   saturation=self.saturation_perif.get(),
                                                   sharpening_itteration=self.sharpening_itteration.get(),
                                                   sharpening_s=self.sharpening_s.get(),
                                                   sharpening_r=self.sharpening_r.get())

            self.image_setter(selector=CodeValues.Modes.B.value, numpy_image=result_B)
            self.image_setter(selector=CodeValues.Modes.P.value, numpy_image=result_P)
            image_pack["Image"][CodeValues.Modes.P] = result_P
        elif mode == CodeValues.ProcessingModes.LOCAL:
            exposure_image_dict = accept_image.image_accepter(image_pack)
            channel_dict = hdr_debevec.hdr_debevec(exposure_image_dict, lambda_=50, num_px=150)
            irradiance_map_dict = irradiance.compute_irradiance(channel_dict, exposure_image_dict)
            result_dict = process_local_tonemap.process_local_tonemap(irradiance_map_dict, saturation=1., gamma=2.2,
                                                                      numtiles=(24, 24))
            image_pack["Image"][CodeValues.Modes.B.value] = result_dict[CodeValues.Modes.B.value]
            image_pack["Image"][CodeValues.Modes.P.value] = result_dict[CodeValues.Modes.P.value]


if __name__ == "__main__":
   gui = App()
   gui.run_app()
