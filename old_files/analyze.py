from plots import *

dirc = "/oasis/tscc/scratch/cchoban/SKIRT_ver_comparison/SKIRT8/"
inst_file = "out_i00_sed.dat"

SED_plot(dirc, inst_file, out_dirc='./', img_name="SED.png", components=['total','transparent','stellar','dust_emission'], SKIRT_ver=8)

calc_IRXBeta(dirc, inst_file)