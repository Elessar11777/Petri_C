from enum import Enum
from resources.Values import CodeValues


class ButtonActions(Enum):
    EXPOSURE_BUTTON = CodeValues.GUITexts.EXPOSURE_BOTTOM.value
    MODES_BUTTON = CodeValues.GUITexts.MODES_BUTTON.value
    POSTPROCESSING_BUTTON = CodeValues.GUITexts.POSTPROCESSING_BUTTON.value
    SETTINGS_SAVE_BUTTON = CodeValues.GUITexts.SETTINGS_SAVE_BUTTON.value

button_widgets = [
    (ButtonActions.EXPOSURE_BUTTON.value, 0.04, 0.9, "normal"),
    (ButtonActions.MODES_BUTTON.value, 0.165, 0.9, "disabled"),
    (ButtonActions.POSTPROCESSING_BUTTON.value, 0.290, 0.9, "normal"),
    (ButtonActions.SETTINGS_SAVE_BUTTON.value, 0.85, 0.9, "normal")
]

segmented_button_widgets =[
    ([CodeValues.GUITexts.GRACIA.value, CodeValues.GUITexts.SPOT.value], 0.05, 0.05),
    ([CodeValues.GUITexts.LOCAL.value, CodeValues.GUITexts.GLOBAL.value, CodeValues.GUITexts.EF.value], 0.05, 0.13)
    ]

segmented_button_logic = [
    (CodeValues.ParameterNames.DEVICE.value, (CodeValues.Device.SPOT.value, CodeValues.GUITexts.SPOT.value), (CodeValues.Device.GRACIA.value, CodeValues.GUITexts.GRACIA.value)),
    (CodeValues.ParameterNames.PROCESSING_MODE.value, (CodeValues.ProcessingModes.LOCAL.value, CodeValues.GUITexts.LOCAL.value, CodeValues.ProcessingModes.EF.value), (CodeValues.ProcessingModes.GLOBAL.value, CodeValues.GUITexts.GLOBAL.value, CodeValues.GUITexts.EF.value))
]

