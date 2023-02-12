import json
import numpy

import HDR_Aligning
import HDR_Test
import HDR_CRF

def CRF_JSON_exporter(crf, path):
    with open(path, 'wb') as f:
        numpy.save(f, crf)
        #json.dump(crf_list, f)
    print(f"CRF exported in {path}")

def CRF_JSON_importer(name):
    with open(name, 'r') as f:
        array = numpy.load(name, allow_pickle=True)
    print("CRF is loaded")
    return array

if __name__ == "__main__":
    cv_images, times = HDR_Test.test_cv_images(selector="KP")
    result_aligning = HDR_Aligning.aligning(cv_images, times)
    CRF = HDR_CRF.CRF_calculate(result_aligning)
    print({f"CRF calculated is /n {CRF}"})

    CRF_JSON_exporter(CRF, path="./images/configs/crf_bottom.npy")
    CRF_imported = CRF_JSON_importer("./images/configs/crf_bottom.npy")
    print(f"CRF imported is /n {CRF_imported}")
