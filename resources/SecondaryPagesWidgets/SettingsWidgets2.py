from enum import Enum
from resources.Values import CodeValues


class ButtonActions(Enum):
    EXPOSURE_BUTTON = CodeValues.GUITexts.EXPOSURE_BOTTOM.value
    MODES_BUTTON = CodeValues.GUITexts.MODES_BUTTON.value
    POSTPROCESSING_BUTTON = CodeValues.GUITexts.POSTPROCESSING_BUTTON.value
    SETTINGS_SAVE_BUTTON = CodeValues.GUITexts.SETTINGS_SAVE_BUTTON.value


button_widgets = [
    (ButtonActions.EXPOSURE_BUTTON.value, 0.025, 0.9, "normal"),
    (ButtonActions.MODES_BUTTON.value, 0.265, 0.9, "normal"),
    (ButtonActions.POSTPROCESSING_BUTTON.value, 0.5, 0.9, "disabled"),
    (ButtonActions.SETTINGS_SAVE_BUTTON.value, 0.75, 0.9, "normal")
]

label_widgets_global = [
    (CodeValues.GUITexts.POSTPROCESSING_LABEL.value, 0.05, 0.05),
    (CodeValues.GUITexts.SHARPENING_ITTERATION_LABEL.value, 0.05, 0.13),
    (CodeValues.GUITexts.SHARPENING_R_LABEL.value, 0.05, 0.21),
    (CodeValues.GUITexts.SHARPENING_S_LABEL.value, 0.05, 0.29),
    (CodeValues.GUITexts.BOTTOM_TONEMAP_LABEL.value, 0.05, 0.37),
    (CodeValues.GUITexts.PERIF_TONEMAP_LABEL.value, 0.05, 0.45)
]

entry_widgets_global = [
    (CodeValues.ParameterNames.SHARPENING_ITTERATION.value, 0.4, 0.13),
    (CodeValues.ParameterNames.SHARPENING_R.value, 0.4, 0.21),
    (CodeValues.ParameterNames.SHARPENING_S.value, 0.4, 0.29),
    (CodeValues.ParameterNames.GAMMA_BOTTOM.value, 0.4, 0.37),
    (CodeValues.ParameterNames.SATURATION_BOTTOM.value, 0.6, 0.37),
    (CodeValues.ParameterNames.GAMMA_PERIF.value, 0.4, 0.45),
    (CodeValues.ParameterNames.SATURATION_PERIF.value, 0.6, 0.45)
]

label_widgets_local = [
    (CodeValues.GUITexts.POSTPROCESSING_LABEL.value, 0.05, 0.05),
    ("HDR Лямбда", 0.05, 0.13),
    ("HDR Пиксели", 0.05, 0.21),
    ("Насыщенность", 0.05, 0.29),
    ("Гамма", 0.05, 0.37),
    ("Патчи", 0.05, 0.45),
]

entry_widgets_local = [
    (CodeValues.ParameterNames.HDR_LAMBDA.value, 0.4, 0.13),
    (CodeValues.ParameterNames.HDR_PIXELS.value, 0.4, 0.21),
    (CodeValues.ParameterNames.LOCAL_SATURATION.value, 0.4, 0.29),
    (CodeValues.ParameterNames.LOCAL_GAMMA.value, 0.4, 0.37),
    (CodeValues.ParameterNames.BATCH_SIZE.value, 0.4, 0.45)

]

