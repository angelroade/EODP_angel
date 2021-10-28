import os

import numpy as np

from common.io.writeToa import readToa
from common.plot.plotF import plotF
from pathlib import Path

def compareTOA(dir_example, dir_executed, fileName):
    example_toa=readToa(dir_example, fileName)
    executed_toa=readToa(dir_executed, fileName)

    diference=np.abs((executed_toa-example_toa)/executed_toa)

    title_str = fileName.replace(".nc", "") + " Difference"
    xlabel_str='TOA Along track'
    ylabel_str='Difference'
    out_dir = os.path.join(dir_executed, "test")
    alt = int(diference.shape[0]/2)
    plotF([], diference[alt,:], title_str, xlabel_str, ylabel_str, out_dir, fileName.replace(".nc", ".png"))

path = Path(os.path.realpath(__file__))
auxdir = '/home/luss/EODP/EODP_angel/auxiliary'
indir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1B/input/'
outdir = '/home/luss/my_shared_folder/test_l1b/'

in_toas = [f for f in os.listdir(indir) if os.path.isfile(os.path.join(indir, f))]
in_toas_path = []

for file in in_toas:
    in_toas_path.append(os.path.join(indir, file))

for name_file in in_toas:
    compareTOA(indir, outdir, name_file)

