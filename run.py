from make_files import *

# Directory of snapshot
sdir = './scripts'
# Output directory
odir = './output'
# Number of snapshot
snum = 600
# Is the snapshot cosmological?
cosmological=1
# ID of halo to use
id = 0
# Is the AHF version old or new?
old_AHF = False
# Do you want to include relative particle velocities for SKIRT
includeVels = True
# Do the snapshots include dust?
importDust = True
# What kind of dust composition do you want to use? (MW, SMC)
dustType = 'SMC'

make_files(sdir, odir, snum, id=id, dusttype='SMC', DTM=1., includeVels=True, importDust=True)