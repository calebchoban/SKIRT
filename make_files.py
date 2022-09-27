
import numpy as np
import xml.etree.ElementTree as ET
import copy
import os
from crc_scripts.gizmo import *

from gadget_lib.load_stellar_hsml import get_particle_hsml

# write particle file
def write_particle_file(sdir, snum, odir, id=-1, cosmological=1, includeVels=True, importDust=True,
                        separateDust=False, hdir=None, PAH_frac = 0.046):
    sp = load_snap(sdir, snum, cosmological=cosmological)

    hl = sp.loadhalo(id=id,hdir=hdir)
    xc, yc, zc, rvir = hl.xc, hl.yc, hl.zc, hl.rvir
    
    p4 = sp.loadpart(4)
    x, y, z = p4.p[:,0]-xc, p4.p[:,1]-yc, p4.p[:,2]-zc
    vx, vy, vz = p4.v[:,0], p4.v[:,1], p4.v[:,2]
    h = get_particle_hsml(x, y, z)
    r = np.sqrt(x**2+y**2+z**2)
    m, Z, t = 1e10*p4.m, p4.z[:,0], 1e9*p4.age

    f = open(odir+"/star.dat", 'w')
    j, = np.where(r<rvir)
    if includeVels:
        header =   '# star.dat \n' + \
                   '# Column 1: position x (pc)\n' + \
                   '# Column 2: position y (pc)\n' + \
                   '# Column 3: position z (pc)\n' + \
                   '# Column 4: smoothing length (pc)\n' + \
                   '# Column 5: velocity x (km/s)\n' + \
                   '# Column 6: velocity y (km/s)\n' + \
                   '# Column 7: velocity z (km/s)\n' + \
                   '# Column 8: mass (Msun)\n' + \
                   '# Column 9: metallicity (1)\n' + \
                   '# Column 10: age (yr)\n'
        f.write(header)
        for i in j:
            line = "%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],vx[i],vy[i],vz[i],m[i],Z[i],t[i])
            f.write(line)
        f.close()
    else:
        header =   '# star.dat \n' + \
                   '# Column 1: position x (pc)\n' + \
                   '# Column 2: position y (pc)\n' + \
                   '# Column 3: position z (pc)\n' + \
                   '# Column 4: smoothing length (pc)\n' + \
                   '# Column 5: mass (Msun)\n' + \
                   '# Column 6: metallicity (mass fraction)\n' + \
                   '# Column 7: age (yr)\n'
        f.write(header)
        for i in j:
            line = "%.2f %.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],Z[i],t[i])
            f.write(line)
        f.close()        

    print("Star data written to star.dat...")

    p0 = sp.loadpart(0)
    x, y, z = p0.p[:,0]-xc, p0.p[:,1]-yc, p0.p[:,2]-zc
    vx, vy, vz = p0.v[:,0], p0.v[:,1], p0.v[:,2]
    # If the snapshots include dust amounts, give those to SKIRT and set DZ to 1
    # Else just assume a constant DZ everywhere
    if importDust:
        h, m, T = p0.h, 1.0e10*p0.m*p0.dz[:,0], p0.T
        if separateDust:
            max_PAH = 0.15 # Set maximum fraction of carbonceous dust which is PAHs
            silm = 1.0e10*p0.m*(p0.spec[:,0]+np.sum(p0.spec[:,2:],axis=1)) # Assume everything not carbonaceous is silicates
            graphm =1.0e10*p0.m*p0.spec[:,1]
            PAHm = graphm*PAH_frac
            graphm -= PAHm
    else:
        h, m, T = p0.h, 1.0e10*p0.m*p0.z[:,0], p0.T
    r = np.sqrt(x**2+y**2+z**2)

    f = open(odir+"/gas.dat", 'w')
    j, = np.where(r<rvir)
    # Make header for gas/dust. Needs to be in this specific order
    header =   '# gas.dat \n' + \
               '# Column 1: position x (pc)\n' + \
               '# Column 2: position y (pc)\n' + \
               '# Column 3: position z (pc)\n' + \
               '# Column 4: smoothing length (pc)\n'
    if separateDust:
            header += '# Column 5: silicate mass (Msun)\n' + \
                      '# Column 6: graphite mass (Msun)\n' + \
                      '# Column 7: PAH mass (Msun)\n' + \
                      '# Column 8: temperature (K)\n'
            if includeVels:
                header +=  '# Column 9: velocity x (km/s)\n' + \
                           '# Column 10: velocity y (km/s)\n' + \
                           '# Column 11: velocity z (km/s)\n'
    else:
            header += '# Column 5: dust mass (Msun)\n' + \
                      '# Column 6: temperature (K)\n'
            if includeVels:
                header +=  '# Column 7: velocity x (km/s)\n' + \
                           '# Column 8: velocity y (km/s)\n' + \
                           '# Column 9: velocity z (km/s)\n'
    f.write(header)

    if includeVels:
        if importDust and separateDust:
            for i in j:
                line = "%.2f %.2f %.2f %.3e %.3e %.3e %.3e %.3e %.2f %.2f %.2f\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],silm[i],graphm[i],PAHm[i],T[i],vx[i],vy[i],vz[i])
                f.write(line)
        else:
            for i in j:
                line = "%.2f %.2f %.2f %.3e %.3e %.3e %.2f %.2f %.2f\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],T[i],vx[i],vy[i],vz[i])
                f.write(line)
        f.close()
    else:
        if importDust and separateDust:
                line = "%.2f %.2f %.2f %.3e %.3e %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],silm[i],graphm[i],PAHm[i],T[i])
                f.write(line)
        else:
            for i in j:
                line = "%.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],T[i])
                f.write(line)
        f.close()

    print("Gas/Dust data written to gas.dat...")

    return

# create parameter file
def write_param_file(fname, dusttype='MW', includeCMB=False, includeVels=True, importDust=True, seperateDust=True,
                     redshift=0.0, hubble=0.702,OmegaMatter=0.3175, DZ=1., gridsize=2e4, maxT=0, LTE=False):

    if not seperateDust:
        infile = "sample/Sample_%s.ski"%dusttype
    else:
        infile = "sample/Sample_Multi.ski"

    tree = ET.parse(infile)
    root = tree.getroot()

    # set the CMB
    # TODO: Check how to add CMB to ski file (looks like they have yet to add this feature, check the github repo)
    """
    eleStellar = root[0][3][0][0]
    eleCMB = eleStellar[1]
    if includeCMB==False:
        eleStellar.remove(eleCMB)
    else:
        T_CMB = 2.7315*(1+redshift)
        R_CMB = 1.733*gridsize # in pc
        L_CMB = 5.670372622e-5*T_CMB**4*4*np.pi*(R_CMB*3.08567758e18)**2/3.839e33 # in Lsun
        eleCMB[0][0].set('backgroundRadius', "%.2f pc"%R_CMB)
        eleCMB[1][0].set('temperature', "%.3f K"%T_CMB)
        eleCMB[2][0].set('luminosity', "%.4e Lsun"%L_CMB)
    """

    # set whether velocity if imported
    eleCosmo = root[0][2][0]
    eleStellar = root[0][3][0][0][0]
    eleDustEmiss =  root[0][4][0][4][0]
    if seperateDust and importDust:
        eleSil = root[0][4][0][5][0]
        eleGraph = root[0][4][0][5][1]
        elePAH= root[0][4][0][5][2]
    else:
        eleGas = root[0][4][0][5][0]

    if LTE:
        eleDustEmiss.set('dustEmissionType','Equilibrium')
    else:
        eleDustEmiss.set('dustEmissionType','Stochastic')

    if redshift > 0:
        eleCosmo.set('redshift',"%.2f"%redshift)
        eleCosmo.set('reducedHubbleConstant',"%.3f"%hubble)
        eleCosmo.set('matterDensityFraction',"%.4f"%OmegaMatter)

    if not includeVels:
        eleStellar.set('importVelocity', 'false')
        eleGas.set('importVelocity', 'false')

    # set dust-to-metal ratio
    if not importDust:
        eleGas.set('massFraction', "%.2f"%DZ)
    if maxT > 0:
        if importDust and seperateDust:
            eleSil.set('maxTemperature', "%.1e K"%maxT)
            eleGraph.set('maxTemperature', "%.1e K"%maxT)
            elePAH.set('maxTemperature', "%.1e K"%maxT)
        else:
            eleGas.set('maxTemperature', "%.1e K"%maxT)


    # set octree
    eleOctree = root[0][4][0][7][0]
    eleOctree.set('minX', "-%.2f pc"%gridsize)
    eleOctree.set('maxX', "%.2f pc"%gridsize)
    eleOctree.set('minY', "-%.2f pc"%gridsize)
    eleOctree.set('maxY', "%.2f pc"%gridsize)
    eleOctree.set('minZ', "-%.2f pc"%gridsize)
    eleOctree.set('maxZ', "%.2f pc"%gridsize)
    tree.write(fname, encoding='UTF-8', xml_declaration=True)

    return

def make_files(sdir, odir, snum, id=-1, dusttype='MW', DZ=1, includeCMB=False, includeVels=True,
               importDust=True, separateDust=True, cosmological=True, hdir=None, maxT=0, LTE=False, PAH_frac=0.046):

    # read snapshot
    sp = load_snap(sdir, snum, cosmological=1)
    if sp.k==-1: return # no snapshot
    hl = sp.loadhalo(id=id, hdir=hdir)

    # create directory
    if not os.path.exists(odir): os.system("mkdir -p %s"%odir)

    # If importing dust want to use all of the dust mass
    if importDust:
        DZ=1.

    # write parameter file
    write_param_file(odir+"/out.ski", dusttype=dusttype, includeCMB=includeCMB, DZ=DZ, includeVels=includeVels,
        importDust=importDust, seperateDust=separateDust, redshift=sp.redshift, gridsize=1e3*hl.rvir, maxT=maxT, LTE=LTE)
    os.system("cp wave.dat %s"%odir)

    # write particle file
    write_particle_file(sdir, snum, odir, id=id, includeVels=includeVels, importDust=importDust,
                        separateDust=separateDust, hdir=hdir, PAH_frac=PAH_frac)

    return
