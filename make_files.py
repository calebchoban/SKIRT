
import numpy as np
import xml.etree.ElementTree as ET
import copy
import os
from gizmo import *
from gadget_lib.load_stellar_hsml import get_particle_hsml

# write particle file
def write_particle_file(sdir, snum, odir, id=0, cosmological=1, includeVels=True, importDust=True):
    sp = loadsnap(sdir, snum, cosmological=cosmological)

    hl = sp.loadhalo(id=id)
    xc, yc, zc, rvir = hl.xc, hl.yc, hl.zc, hl.rvir
    
    p4 = sp.loadpart(4)
    x, y, z = p4.p[:,0]-xc, p4.p[:,1]-yc, p4.p[:,2]-zc
    vx, vy, vz = p4.v[:,0], p4.v[:,1], p4.v[:,2]
    h = get_particle_hsml(x, y, z)
    r = np.sqrt(x**2+y**2+z**2)
    m, Z, t = 1e10*p4.m, p4.z, 1e9*p4.age

    f = open(odir+"/star.dat", 'w')
    j, = np.where(r<rvir)
    if includeVels:
        for i in j:
            line = "%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],vx[i],vy[i],vz[i],m[i],Z[i],t[i])
            f.write(line)
        f.close()
    else:
        for i in j:
            line = "%.2f %.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],Z[i],t[i])
            f.write(line)
        f.close()        

    p0 = sp.loadpart(0)
    x, y, z = p0.p[:,0]-xc, p0.p[:,1]-yc, p0.p[:,2]-zc
    vx, vy, vz = p0.v[:,0], p0.v[:,1], p0.v[:,2]
    # If the snapshots include dust amounts, give those to SKIRT and set DTM to 1
    # Else just assume a constant DTM everywhere
    if importDust:
        h, m, DorZ, T = p0.h, 1.0e10*p0.m, p0.dz[:,0], p0.T
    else:
        h, m, DorZ, T = p0.h, 1.0e10*p0.m, p0.z, p0.T
    r = np.sqrt(x**2+y**2+z**2)

    f = open(odir+"/gas.dat", 'w')
    j, = np.where(r<rvir)
    if includeVels: 
        for i in j:
            line = "%.2f %.2f %.2f %.2f %.3e %.3e %.3e %.2f %.2f %.2f\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],DorZ[i],T[i],vx[i],vy[i],vz[i])
            f.write(line)
        f.close()
    else:
        for i in j:
            line = "%.2f %.2f %.2f %.2f %.3e %.3e %.3e\n" %(1e3*x[i],1e3*y[i],1e3*z[i],1e3*h[i],m[i],DZ[i,0],T[i])
            f.write(line)
        f.close()

    return

# create parameter file
def write_param_file(fname, dusttype='MW', includeCMB=False, includeVels=True, importDust=True, redshift=6.0, 
            DTM=1., gridsize=2e4):
    infile = "sample/Sample_%s.ski"%dusttype
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
    eleStellar = root[0][2][0][0][0]
    eleGas = root[0][3][0][3][0]
    if not includeVels:
        eleStellar.set('importVelocity', 'false')
        eleGas.set('importVelocity', 'false')

    # set dust-to-metal ratio
    if not importDust:
        eleGas.set('massFraction', "%.2f"%DTM)

    # set octree
    eleOctree = root[0][3][0][4][0]
    eleOctree.set('minX', "-%.2f pc"%gridsize)
    eleOctree.set('maxX', "%.2f pc"%gridsize)
    eleOctree.set('minY', "-%.2f pc"%gridsize)
    eleOctree.set('maxY', "%.2f pc"%gridsize)
    eleOctree.set('minZ', "-%.2f pc"%gridsize)
    eleOctree.set('maxZ', "%.2f pc"%gridsize)

    tree.write(fname, encoding='UTF-8', xml_declaration=True)

    return

def make_files(sdir, odir, snum, id=0, dusttype='MW', DTM=1, includeCMB=False, includeVels=True, importDust=True):

    # read snapshot
    sp = loadsnap(sdir, snum, cosmological=1)
    if sp.k==-1: return # no snapshot
    hl = sp.loadhalo(id=id)

    # create directory
    if not os.path.exists(odir): os.system("mkdir -p %s"%odir)

    # write parameter file
    write_param_file(odir+"/out.ski", dusttype=dusttype, includeCMB=includeCMB, DTM=DTM, includeVels=includeVels, 
        importDust=importDust, redshift=sp.redshift, gridsize=1e3*hl.rvir)
    os.system("cp wave.dat %s"%odir)

    # write particle file
    write_particle_file(sdir, snum, odir, id=id, includeVels=includeVels, importDust=importDust)

    return
