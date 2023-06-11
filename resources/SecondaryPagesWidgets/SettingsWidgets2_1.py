from enum import Enum
from resources.Values import CodeValues

class ButtonActions(Enum):
    EXPOSURE_BUTTON = CodeValues.GUITexts.EXPOSURE_BOTTOM.value
    MODES_BUTTON = CodeValues.GUITexts.MODES_BUTTON.value
    POSTPROCESSING_BUTTON = CodeValues.GUITexts.POSTPROCESSING_BUTTON.value
    SETTINGS_SAVE_BUTTON = CodeValues.GUITexts.SETTINGS_SAVE_BUTTON.value


button_widgets = [
    (ButtonActions.EXPOSURE_BUTTON.value, 0.04, 0.9, "normal"),
    (ButtonActions.MODES_BUTTON.value, 0.165, 0.9, "normal"),
    (ButtonActions.POSTPROCESSING_BUTTON.value, 0.290, 0.9, "disabled"),
    (ButtonActions.SETTINGS_SAVE_BUTTON.value, 0.85, 0.9, "normal")
]