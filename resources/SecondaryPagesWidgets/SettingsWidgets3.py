from enum import Enum
from resources.Values.config_creator import configurer


class ButtonActions(Enum):
    EXPOSURE_BUTTON = configurer.GUITexts.EXPOSURE_BUTTON
    MODES_BUTTON = configurer.GUITexts.MODES_BUTTON
    POSTPROCESSING_BUTTON = configurer.GUITexts.POSTPROCESSING_BUTTON
    SETTINGS_SAVE_BUTTON = configurer.GUITexts.SETTINGS_SAVE_BUTTON

button_widgets = [
    (ButtonActions.EXPOSURE_BUTTON, 0.04, 0.9, "normal"),
    (ButtonActions.MODES_BUTTON, 0.165, 0.9, "disabled"),
    (ButtonActions.POSTPROCESSING_BUTTON, 0.290, 0.9, "normal"),
    (ButtonActions.SETTINGS_SAVE_BUTTON, 0.85, 0.9, "normal")
]

segmented_button_widgets =[
    ([configurer.GUITexts.GRACIA, configurer.GUITexts.SPOT], 0.05, 0.05),
    ([configurer.GUITexts.LOCAL, configurer.GUITexts.GLOBAL], 0.05, 0.13)
    ]

segmented_button_logic = [
    (
    configurer.Device,
     (configurer.Device.SPOT, configurer.GUITexts.SPOT),
     (configurer.Device.GRACIA, configurer.GUITexts.GRACIA)
     ),
    (configurer.ProcessingMode,
     (configurer.ProcessingMode.LOCAL, configurer.GUITexts.LOCAL),
     (configurer.ProcessingMode.GLOBAL, configurer.GUITexts.GLOBAL)
     )
]

