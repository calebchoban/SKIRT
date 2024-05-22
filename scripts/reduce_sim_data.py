import numpy as np
import xml.etree.ElementTree as ET
import os
from crc_scripts.utils.stellar_hsml_utils import get_particle_hsml
from crc_scripts.io.gizmo import load_halo

def create_SKIRT_particle_files(snap_dir, snap_num, output_dir, importDust=True):
    '''
    This function extracts and reduces the star and gas particle data from the specified simulation snapshot 
    into SKIRT input file. When extracting dust data it only uses the dust-to-metals (D/Z) ratio.

    Parameters
    ----------
    snap_dir : string
        Name of snapshot directory
    snap_num : int
        Snapshot number
    output_dir : string
        Name of directory where SKIRT outputs will be written to
    importDust : boolean
        Sets whether dust information will be extracted from simulation.
    '''
    # This loads the galactic halo from the snapshot
    halo = load_halo(snap_dir, snap_num, mode='AHF')
    # This orientates the halo so that the galactic disk is face-on
    print("Orientating halo")
    halo.set_orientation()

    if not halo.sp.Flag_DustSpecies and importDust:
        print("WARNING: importDust set to True but this snapshot does not have dust. Set importDust to False.")

    # Load data for star particles (ptype = 4)
    p4 = halo.loadpart(4)
    # x,y,x coordinates
    x, y, z = p4.p[:,0], p4.p[:,1], p4.p[:,2]
    # Compute the star softening lengths. This takes some time.
    print("Calculating star particle smoothing lengths...")
    h = get_particle_hsml(x, y, z)
    # mass, metallicity, and age
    m, Z, t = 1e10*p4.m, p4.z[:,0], 1e9*p4.age

    f = open(output_dir+"/star.dat", 'w')
    # Write header for star file
    header =    '# star.dat \n' + \
                '# Column 1: position x (pc)\n' + \
                '# Column 2: position y (pc)\n' + \
                '# Column 3: position z (pc)\n' + \
                '# Column 4: smoothing length (pc)\n' + \
                '# Column 5: mass (Msun)\n' + \
                '# Column 6: metallicity (1)\n' + \
                '# Column 7: age (yr)\n'
    f.write(header)
    # Step through each star particle and write its data
    for i in range(p4.npart):
        line = "%.2f %.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],Z[i],t[i])
        f.write(line)
    f.close()

    print("Star data written to star.dat...")

    # Load gas particle data (ptype = 0)
    p0 = halo.loadpart(0)
    # x,y,x coordinates
    x, y, z = p0.p[:,0], p0.p[:,1], p0.p[:,2]
    # If the snapshots include dust amounts, give those to SKIRT and set D/Z to 1
    # Else just assume a constant D/Z everywhere.
    if importDust:
        # smoothing length, mass, and temperature
        h, m, T = p0.h, 1.0e10*p0.m*p0.dz[:,0], p0.T
    else:
        # smoothing length, mass, and temperature
        h, m, Z, T = p0.h, 1.0e10*p0.m, p0.z[:,0], p0.T

    f = open(output_dir+"/gas.dat", 'w')
    # Make header for gas/dust. Needs to be in this specific order
    header =   '# gas.dat \n' + \
               '# Column 1: position x (pc)\n' + \
               '# Column 2: position y (pc)\n' + \
               '# Column 3: position z (pc)\n' + \
               '# Column 4: smoothing length (pc)\n'
    if importDust:
        header += '# Column 5: dust mass (Msun)\n' + \
                  '# Column 6: temperature (K)\n'
    else:
        header += '# Column 5: mass (Msun)\n' + \
                  '# Column 6: metallicity (1)\n' + \
                  '# Column 7: temperature (K)\n'
    f.write(header)

    if importDust:
        for i in range(p0.npart):
            line = "%.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],T[i])
            f.write(line)
    else:
        for i in range(p0.npart):
            line = "%.2f %.2f %.2f %.3e %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],Z[i],T[i])
            f.write(line)
    f.close()

    print("Gas/Dust data written to gas.dat...")