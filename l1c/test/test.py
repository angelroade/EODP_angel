import os

import numpy as np

from common.io.writeToa import readToa
from common.plot.plotF import plotF
from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = '/home/luss/EODP/EODP_angel/auxiliary/'
# GM dir + L1B dir
indir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1C/output'
outdir = '/home/luss/my_shared_folder/test_l1c/'

provided_toas = [f for f in os.listdir(indir) if os.path.isfile(os.path.join(indir, f))]
provided_toas_path = []
for file in provided_toas:
    provided_toas_path.append(os.path.join(indir, file))

generated_toas = [f for f in provided_toas if os.path.isfile(os.path.join(outdir, f))]
generated_toas_path = []
for file in generated_toas:
    generated_toas_path.append(os.path.join(outdir, file))

for name_file in generated_toas:
    if "VNIR" in name_file:
        if ".nc" in name_file:
            ref_toa = readToa(indir, name_file)
            ref_toa = np.sort(ref_toa)
            generated_toa = readToa(outdir, name_file)
            generated_toa = np.sort(generated_toa)
            diff_toa = np.abs(generated_toa-ref_toa)

            print("Difference: " + str(np.max(diff_toa)))

