from enum import Enum


class Device(Enum):
    SPOT = "Spot"
    GRACIA = "Gracia"
class Modes(Enum):
    B = "B"
    P = "P"
class ProcessingModes(Enum):
    GLOBAL = "global"
    LOCAL = "local"
class Paths(Enum):
    SETTINGS = './images/configs/settings.json'
    ICON = "./Icon.ico"
    SPOT_IMAGES = "./images/spot-test/"
    GRACIA_IMAGES = "./images/gracia-test/"
    SOURCE_SPOT = "./images/img_source/spot-test/"
    SOURCE_GRACIA = "./images/configs/"
class GUI(Enum):
    MODE = "dark"
    THEME = "dark-blue"
    TITLE = "Aeya"
    SETTINGS_TITLE = "Aeya Настройки"
    GEOMETRY = "1280x720"

    IMAGE_FRAME_FOREGROUND = 'gray'
    IMAGE_FRAME_BORDER = "black"
    BORDER_WIDTH = 5
    WIDTH = 500
    HEIGHT = 500
    # Input field status
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    REACTION_COLOR = "#343638"

    INPUT_TEXT_COLOR = "black"
    INPUT_TEXT_REACTION_COLOR = "white"

class GUITexts(Enum):
    # Modes
    SPOT = "Спот-тест"
    GRACIA = "Метод Грациа"
    # Tonemap Modes
    LOCAL = "Локальное тонирование"
    GLOBAL = "Глобальное тонирование"
    # Camera connection status
    NOT_CONNECTED = "Камера не подключена"
    CONNECTED = "Камера подключена"
    CAMERA_ERROR = "Не удалось открыть устройство"
    # Translation buttons
    START_TRANSLATION_BUTTON = "Начать трансляцию"
    STOP_TRANSLATION_BUTTON = "Прекратить трансляцию"
    # Main page buttons
    TRIGGER_BUTTON = "Триггер"
    FOLDER_BUTTON = "Папка"
    SETTINGS_BUTTON = "Настройки"
    SYNC_BUTTON = "Синхронизация"
    # Settings buttons
    SETTINGS_SAVE_BUTTON = "Сохранить"
    EXPOSURE_BOTTOM = "Экспозиция"
    MODES_BUTTON = "Режимы"
    POSTPROCESSING_BUTTON = "Постобработка"
    CALIBRATION_BUTTON = "Калибровка"

    # Main page labels
    CODE_LABEL = "Код:"
    # Settings labels
    EXPOSURE_BOTTOM_LABEL = "Экспозиция просвет"
    EXPOSURE_PERIF_LABEL = "Экспозиция периферия"
    EXPOSURE_MIN_LABEL = "Минимальная"
    EXPOSURE_MAX_LABEL = "Максимальная"
    EXPOSURE_NUM_LABEL = "Количество"
    EXPOSURE_NUM_CALIBRATION_LABEL = "Количество калибровочное"

    POSTPROCESSING_LABEL = "Постобработка"
    SHARPENING_ITTERATION_LABEL = "Иттерации резкости"
    SHARPENING_R_LABEL = "R резкости"
    SHARPENING_S_LABEL = "S резкости"
    BOTTOM_TONEMAP_LABEL = "Тонирование просвет"
    PERIF_TONEMAP_LABEL = "Тонирование периферия"

class ExposureBottomSettings(Enum):
    EXPOSURE_BOTTOM_MIN = 30000
    EXPOSURE_BOTTOM_MAX = 300000
    EXPOSURE_BOTTOM_NUM = 10
    EXPOSURE_BOTTOM_NUM_CALIBRATION = 100
class ExposurePerifSettings(Enum):
    EXPOSURE_PERIF_MIN = 30000
    EXPOSURE_PERIF_MAX = 800000
    EXPOSURE_PERIF_NUM = 10
    EXPOSURE_PERIF_NUM_CALIBRATION = 100
class SharpeningSettings(Enum):
    SHARPENING_ITTERATION = 2
    SHARPENING_R = 0.2
    SHARPENING_S = 20


class GlobalTonemapBottomSettings(Enum):
    GAMMA_BOTTOM = 1.4
    SATURATION_BOTTOM = 2.0

class GlobalTonemapPerifSettings(Enum):
    GAMMA_PERIF = 2.0
    SATURATION_PERIF = 1.2

class LocalTonemapSettings(Enum):
    LAMBDA = 50
    NUM_PX = 150
    SATURATION = 1.0
    GAMMA = 2.2
    NUM_TILES = (24, 24)

class ParameterNames(Enum):
    EXPOSURE_BOTTOM_MIN = "exposure_bottom_min"
    EXPOSURE_BOTTOM_MAX = "exposure_bottom_max"
    EXPOSURE_BOTTOM_NUM = "exposure_bottom_num"
    EXPOSURE_BOTTOM_NUM_CALIBRATION = "exposure_bottom_num_calibration"
    EXPOSURE_PERIF_MIN = "exposure_perif_min"
    EXPOSURE_PERIF_MAX = "exposure_perif_max"
    EXPOSURE_PERIF_NUM = "exposure_perif_num"
    EXPOSURE_PERIF_NUM_CALIBRATION = "exposure_perif_num_calibration"
    SHARPENING_ITTERATION = "sharpening_itteration"
    SHARPENING_R = "sharpening_r"
    SHARPENING_S = "sharpening_s"
    GAMMA_BOTTOM = "gamma_bottom"
    SATURATION_BOTTOM = "saturation_bottom"
    GAMMA_PERIF = "gamma_perif"
    SATURATION_PERIF = "saturation_perif"
    DEVICE = "device"
    PROCESSING_MODE = "tonemapping"
    HDR_LAMBDA = "HDR_lambda"
    HDR_PIXELS = "HDR_pixels"
    LOCAL_SATURATION = "local_saturation"
    LOCAL_GAMMA = "local_gamma"
    BATCH_SIZE = "batch_size"

    AEYA_SERVER_URL = "aeya_server_url"
    WEB_SERVER_URL = "web_server_url"
    ML_SERVER_URL = "ml_server_url"
    AEYA_SERVER_PORT = "aeya_server_port"
    WEB_SERVER_PORT = "web_server_port"
    ML_SERVER_PORT = "ml_server_port"





class Parameters():
    @staticmethod
    def get_default_parameters():
        return {
            ParameterNames.EXPOSURE_BOTTOM_MIN.value: 30000,
            ParameterNames.EXPOSURE_BOTTOM_MAX.value: 300000,
            ParameterNames.EXPOSURE_BOTTOM_NUM.value: 10,
            ParameterNames.EXPOSURE_BOTTOM_NUM_CALIBRATION.value: 100,
            ParameterNames.EXPOSURE_PERIF_MIN.value: 30000,
            ParameterNames.EXPOSURE_PERIF_MAX.value: 800000,
            ParameterNames.EXPOSURE_PERIF_NUM.value: 10,
            ParameterNames.EXPOSURE_PERIF_NUM_CALIBRATION.value: 100,
            ParameterNames.SHARPENING_ITTERATION.value: 2,
            ParameterNames.SHARPENING_R.value: 0.2,
            ParameterNames.SHARPENING_S.value: 20,
            ParameterNames.GAMMA_BOTTOM.value: 1.4,
            ParameterNames.SATURATION_BOTTOM.value: 2.0,
            ParameterNames.GAMMA_PERIF.value: 2.0,
            ParameterNames.SATURATION_PERIF.value: 1.2,
            ParameterNames.DEVICE.value: "Gracia",
            ParameterNames.PROCESSING_MODE.value: "local",
            "HDR_lambda": 50,
            "HDR_pixels": 150,
            "local_saturation": 1,
            "local_gamma": 2.2,
            "batch_size": 24,
            "aeya_server_url": "http://194.186.150.221/",
            "web_server_url": "http://194.186.150.221/",
            "ml_server_url": "http://194.186.150.221/",
            "aeya_server_port": "1515",
            "web_server_port": "",
            "ml_server_port": "",
        }
