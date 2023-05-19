from enum import Enum


class ButtonActions(Enum):
    EXPOSURE_BUTTON = 1
    MODES_BUTTON = 2
    POSTPROCESSING_BUTTON = 3
    SETTINGS_SAVE_BUTTON = 4

button_widgets = [
    (ButtonActions.EXPOSURE_BUTTON, 0.025, 0.9, "normal"),
    (ButtonActions.MODES_BUTTON, 0.265, 0.9, "disabled"),
    (ButtonActions.POSTPROCESSING_BUTTON, 0.5, 0.9, "normal"),
    (ButtonActions.SETTINGS_SAVE_BUTTON, 0.75, 0.9, "normal")
]
