from enum import Enum
from resources.Values.config_creator import configurer


class ButtonActions(Enum):
    EXPOSURE_BUTTON = configurer.GUITexts.EXPOSURE_BUTTON
    MODES_BUTTON = configurer.GUITexts.MODES_BUTTON
    POSTPROCESSING_BUTTON = configurer.GUITexts.POSTPROCESSING_BUTTON
    SETTINGS_SAVE_BUTTON = configurer.GUITexts.SETTINGS_SAVE_BUTTON


button_widgets = [
    (ButtonActions.EXPOSURE_BUTTON.value, 0.04, 0.9, "normal"),
    (ButtonActions.MODES_BUTTON.value, 0.165, 0.9, "normal"),
    (ButtonActions.POSTPROCESSING_BUTTON.value, 0.290, 0.9, "disabled"),
    (ButtonActions.SETTINGS_SAVE_BUTTON.value, 0.85, 0.9, "normal")
]

label_widgets_global = [
    (configurer.GUITexts.POSTPROCESSING_LABEL, 0.05, 0.05),
    (configurer.GUITexts.SHARPENING_ITTERATION_LABEL, 0.05, 0.13),
    (configurer.GUITexts.SHARPENING_R_LABEL, 0.05, 0.21),
    (configurer.GUITexts.SHARPENING_S_LABEL, 0.05, 0.29),
    (configurer.GUITexts.BOTTOM_TONEMAP_LABEL, 0.05, 0.37),
    (configurer.GUITexts.PERIF_TONEMAP_LABEL, 0.05, 0.45)
]

entry_widgets_global = [
    (configurer.Sharpening.ITTERATION, 0.25, 0.13),
    (configurer.Sharpening.R, 0.25, 0.21),
    (configurer.Sharpening.S, 0.25, 0.29),
    (configurer.GlobalTonemap.BOTTOM.GAMMA, 0.25, 0.37),
    (configurer.GlobalTonemap.BOTTOM.SATURATION, 0.37, 0.37),
    (configurer.GlobalTonemap.PERIF.GAMMA, 0.25, 0.45),
    (configurer.GlobalTonemap.PERIF.SATURATION, 0.37, 0.45)
]

label_widgets_local = [
    (configurer.GUITexts.POSTPROCESSING_LABEL, 0.05, 0.05),
    ("HDR Лямбда", 0.05, 0.13),
    ("HDR Пиксели", 0.05, 0.21),
    ("Насыщенность", 0.05, 0.29),
    ("Гамма", 0.05, 0.37),
    ("Патчи", 0.05, 0.45),
]

entry_widgets_local = [
    (configurer.ParameterNames.HDR_LAMBDA, 0.25, 0.13),
    (configurer.ParameterNames.HDR_PIXELS, 0.25, 0.21),
    (configurer.ParameterNames.LOCAL_SATURATION, 0.25, 0.29),
    (configurer.ParameterNames.LOCAL_GAMMA, 0.25, 0.37),
    (configurer.ParameterNames.BATCH_SIZE, 0.25, 0.45)

]

