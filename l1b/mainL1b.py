
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = '/home/luss/EODP/EODP_angel/auxiliary'
indir = '/home/luss/my_shared_folder/test_E2E/ISM_module/'
outdir = '/home/luss/my_shared_folder/test_E2E/L1B_module/'

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
