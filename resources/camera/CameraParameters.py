from resources.Values import CameraValues
import gxipy as gx
from logger import aeya_logger


def set_parameters(camera):
    camera.stream_off()
    camera.Width.set(CameraValues.CameraParameters.WIDTH.value)
    camera.Height.set(CameraValues.CameraParameters.HEIGHT.value)
    camera.OffsetX.set(CameraValues.CameraParameters.OFFSET_X.value)
    camera.OffsetY.set(CameraValues.CameraParameters.OFFSET_Y.value)
    camera.PixelFormat.set(CameraValues.CameraParameters.PIXEL_FORMAT.value)
    camera.AcquisitionMode.set(CameraValues.CameraParameters.ACQUISITION_MODE.value)
    camera.ExposureMode.set(CameraValues.CameraParameters.EXPOSURE_MODE.value)
    camera.BalanceWhiteAuto.set(CameraValues.CameraParameters.BALANCE_WHITE_AUTO.value)
    camera.ExposureAuto.set(CameraValues.CameraParameters.EXPOSURE_AUTO.value)

    camera.TriggerMode.set(CameraValues.CameraParameters.TRIGGER_MODE.value)
    camera.TriggerSource.set(CameraValues.CameraParameters.TRIGGER_SOURCE_FIRM.value)

    camera.TriggerActivation.set(CameraValues.CameraParameters.TRIGGER_ACTIVATION.value)
    camera.TriggerFilterRaisingEdge.set(CameraValues.CameraParameters.TRIGGER_FILTER.value)
    camera.stream_on()


def set_parameters_bottom(camera):
    try:
        camera.ExpectedGrayValue.set(250)
        camera.AWBLampHouse.set(gx.GxAWBLampHouseEntry.INCANDESCENT)
        camera.LUTEnable.set(False)
    except Exception as e:
        aeya_logger.error(e)

def set_parameters_perif(camera):
    try:
        camera.ExpectedGrayValue.set(200)
        camera.AWBLampHouse.set(gx.GxAWBLampHouseEntry.D50)
        camera.LUTEnable.set(True)
        gamma_lut = None
        if camera.ContrastParam.is_readable():
            contrast_value = camera.ContrastParam.get()
            contrast_lut = gx.Utility.get_contrast_lut(contrast_value)

        else:
            contrast_lut = None

        color_correction = 0

        return gamma_lut, contrast_lut, color_correction
    except Exception as e:
        aeya_logger.error(e)
