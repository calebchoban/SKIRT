from make_files import *

# Directory of snapshot
sdir = './scripts'
sdir = '/oasis/tscc/scratch/cchoban/FIRE2_wind_tests/extended_AGB_winds/output/'
# Output directory
odir = './output'
# AHF halo directory
hdir ='./halo'
hdir='/oasis/tscc/scratch/cchoban/FIRE2_wind_tests/extended_AGB_winds/AHF_data/AHF_output/'
# Number of snapshot
snum = 600
# Is the snapshot cosmological?
cosmological=1
# ID of halo to use (-1 is most massive fully resolved halo)
id = -1
# Do you want to include relative particle velocities for SKIRT
includeVels = True
# Do the snapshots include dust?
importDust = True
# What kind of dust composition do you want to use? (MW, SMC)
dustType = 'MW'

make_files(sdir, odir, snum, id=id, dusttype=dustType, DTM=1., includeVels=includeVels, importDust=importDust,
		   cosmological=cosmological, hdir=hdir)