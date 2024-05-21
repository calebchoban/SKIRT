from make_files import *

# Directory of snapshot
sdir = './scripts'
sdir = '/oasis/tscc/scratch/cchoban/FIRE2_wind_tests/extended_AGB_winds/output/'
# Output directory for SKIRT
odir = './assumed_dust_output'
# AHF halo directory
hdir ='./halo'
hdir='/oasis/tscc/scratch/cchoban/FIRE2_wind_tests/extended_AGB_winds/AHF_data/AHF_output/'
# Number of snapshot
snum = 600
# Is the snapshot cosmological?
cosmological = 1
# ID of halo to use (-1 is most massive fully resolved halo)
id = -1
# Do you want to include relative particle velocities for SKIRT
includeVels = True
# Use this to set a constant dust-to-metals ratio (this is ignored if you import dust)
DZ = 0.5
# If simulation used 'live' dust evolution you can import the tracked dust mass instead of assuming a constant DZ
importDust = False
# Set dust composition for either assumed DZ or only importing total dust mass (MW, SMC)
dustType = 'MW'
# Do you want to instead separate total dust mass into separate species masses? (this supersedes dustType)
separateDust = True
# Mass fraction of carbonacous dust mass in PAHs, needed for separateDust since we don't explicitly track PAHs
# For the MW qPAH=4.6% (fraction of total dust mass) which for 2-to-1 silicate to carbonaceous dust mass gives 14% of the total carbonaceous dust mass
PAH_frac = 0.14
# Max gas temperature to allow dust (0 K allows all gas to have dust)
maxT = 1E5
# Set whether dust is assumed to be in LTE or non-LTE (default)
LTE = False
# Determine the range of log-space wavelength grid for you mock observations
minWavelength = 0.08
maxWavelength = 1E3
wavebins = 200


make_files(sdir, odir, snum, id=id, dusttype=dustType, DZ=DZ, includeVels=includeVels, importDust=importDust,
		   cosmological=cosmological, hdir=hdir, separateDust=separateDust, maxT=maxT, LTE=LTE, PAH_frac=PAH_frac)

odir = './import_separate_dust'
maxT=0
importDust=True
separateDust=True
make_files(sdir, odir, snum, id=id, dusttype=dustType, DZ=DZ, includeVels=includeVels, importDust=importDust,
		   cosmological=cosmological, hdir=hdir, separateDust=separateDust, maxT=maxT, LTE=LTE, PAH_frac=PAH_frac)

odir = './import_DZ_dust'
maxT=0
importDust=True
separateDust=False
make_files(sdir, odir, snum, id=id, dusttype=dustType, DZ=DZ, includeVels=includeVels, importDust=importDust,
		   cosmological=cosmological, hdir=hdir, separateDust=separateDust, maxT=maxT, LTE=LTE, PAH_frac=PAH_frac)