
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from pymo.data.spectra import SwanSpecFile
import xarray as xr
from pymsl.data

filenames = ['20160512_06z/crux.spec', '20160512_06z/prelud.spec']
for filename in filenames:
    spectra = SwanSpecFile(filename)
    specs = list()
    for spec in spectra.readall():
        specs.append(spec)

    times = spectra.times
    freqs = specs[0].freqs
    dirs = specs[0].dirs

    spectra.close()

    spec_1d = np.array([spec.oned().S.ravel() for spec in specs])
    levs = np.linspace(0, spec_1d.max(), 20)

    plt.figure(figsize=((15,8)))
    plt.contourf(times, 1./freqs, spec_1d.T, levels=levs)
    plt.title(filename)
    plt.grid()

plt.show()


# Gridded data
dset = xr.open_dataset('20160512_06z/nwwa20160512_06z.nc')
dset.hs_sea = np.sqrt(dset.hs**2 - dset.hs_sw**2)

# Check boundary
filename = '20160512_06z/nwwa20160512_06z.bnd.swn'
spectra = SwanSpecFile(filename)
specs = list()
for spec in spectra.readall():
    specs.append(spec)

loc = spectra.locations
times = spectra.times
freqs = specs[0][0].freqs
dirs = specs[0][0].dirs

spectra.close()

x = np.array([site.x for site in loc])
y = np.array([site.y for site in loc])

xsite = 123.5
ysite = -13.5

dist = np.sqrt((x-xsite)**2 + (y-ysite)**2)
ibnd = np.argmin(dist)

spec_1d = np.array([s[ibnd].oned().S.ravel() for s in specs])

plt.figure(figsize=((15,8)))
plt.contourf(times, 1./freqs, spec_1d.T, levels=levs)
plt.title('x=%g, y=%g' % (xsite, ysite))
plt.grid()