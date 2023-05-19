from enum import Enum
import gxipy as gx

class CameraParameters(Enum):
    WIDTH = 2064
    HEIGHT = 2064
    OFFSET_X = 496
    OFFSET_Y = 0
    PIXEL_FORMAT = gx.GxPixelFormatEntry.BAYER_RG10
    ACQUISITION_MODE = gx.GxAcquisitionModeEntry.CONTINUOUS
    EXPOSURE_MODE = gx.GxExposureModeEntry.TIMED
    BALANCE_WHITE_AUTO = gx.GxAutoEntry.CONTINUOUS
    EXPOSURE_AUTO = gx.GxAutoEntry.OFF
    TRIGGER_MODE = gx.GxSwitchEntry.ON
    TRIGGER_SOURCE_FIRM = gx.GxTriggerSourceEntry.LINE0
    TRIGGER_SOURCE_SOFT = gx.GxTriggerSourceEntry.SOFTWARE
    TRIGGER_ACTIVATION = 1
    TRIGGER_FILTER = 5000
    GRAY_BOTTOM = 250
    GRAY_PERIF = 200
    AWB_LAMP_HOUSE_BOTTOM = gx.GxAWBLampHouseEntry.INCANDESCENT
    AWB_LAMP_HOUSE_PERIF = gx.GxAWBLampHouseEntry.D50
