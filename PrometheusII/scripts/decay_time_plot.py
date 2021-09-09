import time
import sys,os
import math
import json
import glob

import datetime

from matplotlib import pyplot as plt

filenames = []

for path in sys.argv[1:]:
    filenames.extend(glob.glob(path))

xlim = [1000,-1000]

bias_remap = False

fig, ax = plt.subplots()
ax2 = ax.twinx()

for filename in filenames:

    with open(filename, 'r') as fp:
        raw = json.load(fp)

    label = raw.get('title', os.path.basename(filename))
    data = raw['data']
    data = list(filter(lambda x: x['valid'] != 0, data))
#    data = list(filter(lambda x: x['bias_max'] < -6.6, data))   

    def bias_map(x):
        return 1.037594*x + .04203

    zvals = [(x['bias_min']+x['bias_max'])/2 for x in data]
    zmin = [ x['bias_max'] for x in data]
    zmax = [ x['bias_max'] for x in data]
    if bias_remap:
        zvals = [bias_map(x) for x in zvals]
        zmin = [bias_map(x) for x in zmin]
        zmax = [bias_map(x) for x in zmax]

    zmin = [x-y for x,y in zip(zvals, zmin)]
    zmax = [x-y for x,y in zip(zvals, zmax)]

    xvals = [datetime.datetime.fromtimestamp(x['timestamp']/1000) for x in data]
    yvals = [x['duration']*1000 for x in data]

#    xlim[0] = min(xlim[0], min(xvals))
#    xlim[1] = max(xlim[1], max(xvals))

    ax.scatter(xvals, yvals, s=2, label="Decay", alpha = 0.5, c='r')
#    ax2.scatter(xvals, zvals, s=2, label="Bias", alpha = 0.5)
    ax2.errorbar(xvals, zvals, [zmin, zmax], label="Bias", alpha = 0.5)

ax.set_title('Measured filter decay times')
ax.set_xlabel('Measurement start time')
ax.set_ylabel('Decay Time (ms)')
#plt.xlim(*xlim)
fig.legend()
ax.grid(True)
ax.grid(True, which='minor', axis='y')
#ax.set_yscale('log')
plt.show()

