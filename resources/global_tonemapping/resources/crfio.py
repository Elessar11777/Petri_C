import numpy


def CRF_exporter(crf, path):
    """
    This function exports the Camera Response Function (CRF) to a specified path.

    Parameters:
    crf (numpy.ndarray): A numpy array representing the CRF.
    path (str): The file path where the CRF will be saved.
    """
    with open(path, 'wb') as f:
        numpy.save(f, crf)  # Save the CRF array to a binary file in NumPy .npy format.
    print(f"CRF exported in {path}")


def CRF_importer(name):
    """
    This function imports the CRF from a specified path.

    Parameters:
    name (str): The file path from where the CRF will be loaded.

    Returns:
    numpy.ndarray: A numpy array representing the CRF.
    """
    with open(name, 'r') as f:
        array = numpy.load(name, allow_pickle=True)  # Load the CRF array from a binary file in NumPy .npy format.
    print("CRF is loaded")
    return array

