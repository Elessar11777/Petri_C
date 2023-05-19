from enum import Enum
from resources.Values import CodeValues


class ButtonActions(Enum):
    SETTINGS_SAVE_BUTTON = 1
    EXPOSURE_BOTTOM = 2
    MODES_BUTTON = 3
    POSTPROCESSING_BUTTON = 4
    CALIBRATION_BUTTON_B = 5
    CALIBRATION_BUTTON_P = 6

button_widgets = [
    (ButtonActions.SETTINGS_SAVE_BUTTON, 0.75, 0.9, "normal"),
    (ButtonActions.EXPOSURE_BOTTOM, 0.025, 0.9, "disabled"),
    (ButtonActions.MODES_BUTTON, 0.265, 0.9, "normal"),
    (ButtonActions.POSTPROCESSING_BUTTON, 0.5, 0.9, "normal"),
    (ButtonActions.CALIBRATION_BUTTON_B, 0.65, 0.37, "normal"),
    (ButtonActions.CALIBRATION_BUTTON_P, 0.65, 0.77, "normal"),
]

label_widgets = [
        (Values.GUITexts.EXPOSURE_BOTTOM_LABEL.value, 0.05, 0.05),
        (Values.GUITexts.EXPOSURE_MIN_LABEL.value, 0.05, 0.13),
        (Values.GUITexts.EXPOSURE_MIN_LABEL.value, 0.4, 0.13),
        (Values.GUITexts.EXPOSURE_MAX_LABEL.value, 0.05, 0.21),
        (Values.GUITexts.EXPOSURE_NUM_LABEL.value, 0.05, 0.29),
        (Values.GUITexts.EXPOSURE_NUM_CALIBRATION_LABEL.value, 0.05, 0.37),
        (Values.GUITexts.EXPOSURE_PERIF_LABEL.value, 0.05, 0.45),
        (Values.GUITexts.EXPOSURE_MIN_LABEL.value, 0.05, 0.53),
        (Values.GUITexts.EXPOSURE_MAX_LABEL.value, 0.05, 0.61),
        (Values.GUITexts.EXPOSURE_NUM_LABEL.value, 0.05, 0.69),
        (Values.GUITexts.EXPOSURE_NUM_CALIBRATION_LABEL.value, 0.05, 0.77),
    ]

entry_widgets = [
    (Values.ParameterNames.EXPOSURE_BOTTOM_MAX.value, 0.4, 0.21),
    (Values.ParameterNames.EXPOSURE_BOTTOM_NUM.value, 0.4, 0.29),
    (Values.ParameterNames.EXPOSURE_BOTTOM_NUM_CALIBRATION.value, 0.4, 0.37),
    (Values.ParameterNames.EXPOSURE_PERIF_MAX.value, 0.4, 0.61),
    (Values.ParameterNames.EXPOSURE_PERIF_NUM.value, 0.4, 0.69),
    (Values.ParameterNames.EXPOSURE_PERIF_NUM_CALIBRATION.value, 0.4, 0.77),
]