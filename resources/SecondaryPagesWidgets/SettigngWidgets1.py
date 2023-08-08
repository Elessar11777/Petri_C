from enum import Enum
from resources.Values import CodeValues
from resources.Values import CameraValues


class ButtonActions(Enum):
    SETTINGS_SAVE_BUTTON = CodeValues.GUITexts.SETTINGS_SAVE_BUTTON.value
    EXPOSURE_BOTTOM = CodeValues.GUITexts.EXPOSURE_BOTTOM.value
    MODES_BUTTON = CodeValues.GUITexts.MODES_BUTTON.value
    POSTPROCESSING_BUTTON = CodeValues.GUITexts.POSTPROCESSING_BUTTON.value
    CALIBRATION_BUTTON_B = CodeValues.GUITexts.CALIBRATION_BUTTON.value
    CALIBRATION_BUTTON_P = CodeValues.GUITexts.CALIBRATION_BUTTON.value

button_widgets = [
    (ButtonActions.SETTINGS_SAVE_BUTTON.value, 0.85, 0.9, "normal"),
    (ButtonActions.EXPOSURE_BOTTOM.value, 0.04, 0.9, "disabled"),
    (ButtonActions.MODES_BUTTON.value, 0.165, 0.9, "normal"),
    (ButtonActions.POSTPROCESSING_BUTTON.value, 0.290, 0.9, "normal"),
    (ButtonActions.CALIBRATION_BUTTON_B.value, 0.4, 0.37, "normal"),
    (ButtonActions.CALIBRATION_BUTTON_P.value, 0.4, 0.77, "normal"),
]

label_widgets = [
        (CodeValues.GUITexts.EXPOSURE_BOTTOM_LABEL.value, 0.05, 0.05),
        (CodeValues.GUITexts.EXPOSURE_MIN_LABEL.value, 0.05, 0.13),
        (CodeValues.GUITexts.EXPOSURE_MAX_LABEL.value, 0.05, 0.21),
        (CodeValues.GUITexts.EXPOSURE_NUM_LABEL.value, 0.05, 0.29),
        (CodeValues.GUITexts.EXPOSURE_NUM_CALIBRATION_LABEL.value, 0.05, 0.37),
        (CodeValues.GUITexts.EXPOSURE_PERIF_LABEL.value, 0.05, 0.45),
        (CodeValues.GUITexts.EXPOSURE_MIN_LABEL.value, 0.05, 0.53),
        (CodeValues.GUITexts.EXPOSURE_MAX_LABEL.value, 0.05, 0.61),
        (CodeValues.GUITexts.EXPOSURE_NUM_LABEL.value, 0.05, 0.69),
        (CodeValues.GUITexts.EXPOSURE_NUM_CALIBRATION_LABEL.value, 0.05, 0.77),

        ("Смещение кадра", 0.6, 0.05),
        ("По ширине", 0.6, 0.13),
        ("По высоте", 0.6, 0.21),
    ]

entry_widgets = [
    (CodeValues.ParameterNames.EXPOSURE_BOTTOM_MIN.value, 0.25, 0.13),
    (CodeValues.ParameterNames.EXPOSURE_BOTTOM_MAX.value, 0.25, 0.21),
    (CodeValues.ParameterNames.EXPOSURE_BOTTOM_NUM.value, 0.25, 0.29),
    (CodeValues.ParameterNames.EXPOSURE_BOTTOM_NUM_CALIBRATION.value, 0.25, 0.37),
    (CodeValues.ParameterNames.EXPOSURE_PERIF_MIN.value, 0.25, 0.53),
    (CodeValues.ParameterNames.EXPOSURE_PERIF_MAX.value, 0.25, 0.61),
    (CodeValues.ParameterNames.EXPOSURE_PERIF_NUM.value, 0.25, 0.69),
    (CodeValues.ParameterNames.EXPOSURE_PERIF_NUM_CALIBRATION.value, 0.25, 0.77),
    (CodeValues.ParameterNames.X_OFFSET.value, 0.8, 0.13),
    (CodeValues.ParameterNames.Y_OFFSET.value, 0.8, 0.21)
]