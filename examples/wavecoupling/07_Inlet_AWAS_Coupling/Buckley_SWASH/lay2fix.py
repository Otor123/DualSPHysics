# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:28:33 2024

@author: user
"""
# Clear all variables from the local namespace
for var in list(locals()):
    del locals()[var]

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


    
nlay = 10
dep = 0.7396
dpx = 0.01
dpz = dep / nlay
firstline = np.zeros(nlay + 2)

gain = 1  # factor to amplify SWASH signal

# file names
# x coupling =17m
velname = 'Buckley_OBC_SWASH.vel'
etaname = 'Buckley_OBC_SWASH.tbl'
awasname = 'Buckley_OBC_SWASH.tbla'

F = open(velname)
TEMP = np.loadtxt(F, skiprows=10, unpack=True)
VELS = np.flip(TEMP[:nlay], axis=0)
VELS_inverted = np.transpose(VELS);

ETA = np.loadtxt(etaname)
VELF = np.zeros((len(ETA), nlay + 1))
for j in range(len(ETA)):
    VELF[j, 0] = VELS_inverted[j, 0]  # Assuming VELF and VELS are already defined
    for i in range(1, nlay + 1):
        x_interp = np.arange((ETA[j, 1] + dep) / nlay / 2, (ETA[j, 1] + dep) * (1 - 1 / nlay / 2)+(ETA[j, 1] + dep) / nlay, (ETA[j, 1] + dep) / nlay)
        y_interp = VELS_inverted[j, :nlay]
        interpolated_value = np.interp(dep * (i - 1) / nlay,  x_interp, y_interp, left=None, right=None, period=None)
        VELF[j, i-1] = interpolated_value

VELF[:, -1] = VELS_inverted[:, -1]

OUT = np.zeros((len(ETA), nlay + 2))
OUT[:, 0] = ETA[:, 0] - ETA[0, 0]
OUT[:, 1:] = VELF * gain

INC_io_name = 'CaseBuckley_inlet.csv'
with open(INC_io_name, 'wt') as fid:
    fid.write('fmtversion;grid_dpx;grid_dpz;grid_nx;grid_nz;vars\n')
    T = [dpx, dpz, 1, nlay + 1]
    fid.write(f'1;{T[0]:.4f};{T[1]:.5f};{T[2]};{T[3]};velx\n\n')
    fid.write('time;vx_x0_z0;vx_x0_z1;vx_x0_z2;vx_x0_z3;vx_x0_z4;vx_x0_z5;vx_x0_z6;vx_x0_z7;vx_x0_z8;vx_x0_z9;vx_x0_z10;vz_x0_z0;vz_x0_z1;vz_x0_z2;vz_x0_z3;vz_x0_z4;vz_x0_z5;vz_x0_z6;vz_x0_z7;vz_x0_z8;vz_x0_z9;vz_x0_z10\n')
    for row in OUT:
        fid.write(f'%.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f\n' % tuple(row))

ETAinc = np.zeros_like(ETA)
ETAinc[:, 1] = ETA[:, 1] * gain + dep
ETAinc[:, 0] = ETA[:, 0] - ETA[0, 0]
np.savetxt('CaseBuckley_zsurf.csv', ETAinc, delimiter=',')

ETAa = np.loadtxt(awasname)
ETAa[:, 1] = ETAa[:, 1] * gain + dep
ETAa[:, 0] = ETAa[:, 0] - ETAa[0, 0]
np.savetxt('CaseBuckley_awasIn.csv', ETAa, delimiter=',')

# Plot
fg1 = plt.figure()
figsize = (10, 6)
plt.figure(figsize=figsize)
plt.plot(OUT[:, 0], VELF[:, -1], 'k', label='SWL')
plt.plot(OUT[:, 0], VELS_inverted[:, -1], '--r', label='Top SWASH')
plt.plot(OUT[:, 0], VELF[:, -2], 'b', label='SWL-dz')
plt.plot(OUT[:, 0], VELS_inverted[:, -2], '--m', label='Top SWASH-1')
plt.plot(OUT[:, 0], VELF[:, -3], 'g', label='SWL-2dz')
plt.plot(OUT[:, 0], VELS_inverted[:, -3], '--c', label='Top SWASH-2')
plt.legend()
plt.xlabel('time (s)')
plt.ylabel('u (m/s)')
plt.xlim([150, 200])
plt.title('Velocities for Inlet')
plt.show()
