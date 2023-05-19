from enum import Enum
from resources.Values import CodeValues


class ButtonActions(Enum):
    EXPOSURE_BUTTON = 1
    MODES_BUTTON = 2
    POSTPROCESSING_BUTTON = 3
    SETTINGS_SAVE_BUTTON = 4


button_widgets = [
    (ButtonActions.EXPOSURE_BUTTON, 0.025, 0.9, "normal"),
    (ButtonActions.MODES_BUTTON, 0.265, 0.9, "normal"),
    (ButtonActions.POSTPROCESSING_BUTTON, 0.5, 0.9, "disabled"),
    (ButtonActions.SETTINGS_SAVE_BUTTON, 0.75, 0.9, "normal")
]

label_widgets = [
    (Values.GUITexts.POSTPROCESSING_LABEL.value, 0.05, 0.05),
    (Values.GUITexts.SHARPENING_ITTERATION_LABEL.value, 0.05, 0.13),
    (Values.GUITexts.SHARPENING_R_LABEL.value, 0.05, 0.21),
    (Values.GUITexts.SHARPENING_S_LABEL.value, 0.05, 0.29),
    (Values.GUITexts.BOTTOM_TONEMAP_LABEL.value, 0.05, 0.37),
    (Values.GUITexts.PERIF_TONEMAP_LABEL.value, 0.05, 0.45)
]

entry_widgets = [
    (Values.ParameterNames.SHARPENING_ITTERATION, 0.4, 0.13),
    (Values.ParameterNames.SHARPENING_R, 0.4, 0.21),
    (Values.ParameterNames.SHARPENING_S, 0.4, 0.29),
    (Values.ParameterNames.GAMMA_BOTTOM, 0.4, 0.37),
    (Values.ParameterNames.SATURATION_BOTTOM, 0.6, 0.37),
    (Values.ParameterNames.GAMMA_PERIF, 0.4, 0.45),
    (Values.ParameterNames.SATURATION_PERIF, 0.6, 0.45)
]
