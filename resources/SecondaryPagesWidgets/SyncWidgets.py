from enum import Enum
from resources.Values import CodeValues

class ButtonActions(Enum):
    SETTINGS_SAVE_BUTTON = CodeValues.GUITexts.SETTINGS_SAVE_BUTTON.value

button_widgets = [
    (ButtonActions.SETTINGS_SAVE_BUTTON.value, 0.85, 0.9, "normal")
]

label_widgets = [
    ("URL Сервера Aeya", 0.05, 0.05),
    ("URL Сервера Web", 0.05, 0.13),
    ("URL Сервера ML", 0.05, 0.21),
    ("GMIC", 0.05, 0.29),
    ("Путь", 0.05, 0.37),
    ("Сжатие", 0.05, 0.45),
    ("R-правило Грациа", 0.05, 0.53),
    ("R-правило Спот", 0.05, 0.61),
]

entry_widgets = [
    ("aeya_server_url", 0.25, 0.05),
    ("web_server_url", 0.25, 0.13),
    ("ml_server_url", 0.25, 0.21),
    ("aeya_server_port", 0.37, 0.05),
    ("web_server_port", 0.37, 0.13),
    ("ml_server_port", 0.37, 0.21),
    ("gmic", 0.25, 0.29),
    ("root", 0.25, 0.37),
    ("compression", 0.25, 0.45),
    ("gracia_string_rule", 0.25, 0.53),
    ("spot_string_rule", 0.25, 0.61),
]