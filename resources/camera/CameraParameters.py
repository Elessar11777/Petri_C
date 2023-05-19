from resources.Values import CameraValues
import gxipy as gx


def set_parameters(camera):
    camera.Width.set(CameraValues.CameraParameters.WIDTH)
    camera.Height.set(CameraValues.CameraParameters.HEIGHT)
    camera.OffsetX.set(CameraValues.CameraParameters.OFFSET_X)
    camera.OffsetY.set(CameraValues.CameraParameters.OFFSET_Y)
    camera.PixelFormat.set(CameraValues.CameraParameters.PIXEL_FORMAT)
    camera.AcquisitionMode.set(CameraValues.CameraParameters.ACQUISITION_MODE)
    camera.ExposureMode.set(CameraValues.CameraParameters.EXPOSURE_MODE)
    camera.BalanceWhiteAuto.set(CameraValues.CameraParameters.BALANCE_WHITE_AUTO)
    camera.ExposureAuto.set(CameraValues.CameraParameters.EXPOSURE_AUTO)

    camera.TriggerMode.set(CameraValues.CameraParameters.TRIGGER_MODE)
    camera.TriggerSource.set(CameraValues.CameraParameters.TRIGGER_SOURCE_FIRM)

    camera.TriggerActivation.set(CameraValues.CameraParameters.TRIGGER_ACTIVATION)
    camera.TriggerFilterRaisingEdge.set(CameraValues.CameraParameters.TRIGGER_FILTER)


def set_parameters_bottom(self):
    self.cam.ExpectedGrayValue.set(250)
    self.cam.AWBLampHouse.set(gx.GxAWBLampHouseEntry.INCANDESCENT)
    self.cam.LUTEnable.set(False)


def set_parameters_perif(camera):
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
