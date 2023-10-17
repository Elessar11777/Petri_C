from .resources.crfio import CRF_importer, CRF_exporter
from .resources.hdr_merge import merging
from .resources.ldr_sharpen import LDR_sharpen
from .resources.tonemaping import tonemaping
from .resources.crf_calc import CRF_calculate


def processor(source, selector, gamma, saturation, sharpening_iteration, s, r, mode="processing",
              crf_bottom_path="../config/crf_bottom.npy", crf_perif_path="../config/crf_perif.npy"):
    """
    Processes a collection of images with specified parameters.
    The function handles multi-exposure image processing tasks.

    Parameters
    ----------
    source : tuple or dict
        The source of the image(s) to be processed.
        If it is a tuple, it should be in the format (exposure_list, image_list).
        If it is a dict, it should be a mapping from exposure values to corresponding images.

    selector : str
        Defines the Camera Response Function (CRF) to be used. Can take the following values:
        'B': Uses the bottom CRF. The function will import the CRF from `../config/crf_bottom.npy`.
        'P': Uses the peripheral CRF. The function will import the CRF from `../config/crf_perif.npy`.

    gamma : float
        The gamma value to be used in the tone mapping stage of the processing.

    saturation : float
        The saturation value to be used in the tone mapping stage of the processing.

    sharpening_iteration : int
        The number of iterations for the sharpening process.

    s : int
        A parameter for the LDR sharpening function.

    r : float
        A parameter for the LDR sharpening function.

    mode : str, optional
        Can be either "processing" or "calibration". Default is "processing".

    crf_bottom_path : str, optional
        File path to import the bottom CRF.

    crf_perif_path : str, optional
        File path to import the peripheral CRF.

    Returns
    -------
    result_sharpening : ndarray
        The final processed image after merging, tone mapping, and sharpening.
    """
    # Ensure source is in expected format
    if isinstance(source, tuple):
        pass
    elif isinstance(source, dict):
        exposure_list = list(source.keys())
        image_list = list(source.values())
        source = (exposure_list, image_list)
    else:
        raise ValueError("Source must be a tuple or dictionary")

    if mode == "processing":
        # Import appropriate CRF based on selector
        if selector == "B":
            try:
                crf = CRF_importer(crf_bottom_path)
            except FileNotFoundError:
                raise FileNotFoundError(f"No file found at {crf_bottom_path}")
        elif selector == "P":
            try:
                crf = CRF_importer(crf_perif_path)
            except FileNotFoundError:
                raise FileNotFoundError(f"No file found at {crf_perif_path}")
        else:
            raise ValueError("Selector must be either 'B' or 'P'")

        # Process image
        result_merging = merging(source, crf)
        result_tonemapping = tonemaping(hdr=result_merging, gamma=float(gamma), saturation=float(saturation))
        result_sharpening = LDR_sharpen(result_tonemapping, iter=int(sharpening_iteration), s=int(s), r=float(r))

        return result_sharpening

    elif mode == "calibration":
        crf = CRF_calculate(source)
        if selector == "B":
            CRF_exporter(crf, path=crf_bottom_path)
            return crf
        elif selector == "P":
            CRF_exporter(crf, path=crf_perif_path)
            return crf

    else:
        raise ValueError("Mode must be either 'processing' or 'calibration'")

