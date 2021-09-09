import time
import sys,os
import math
import json
import glob

from matplotlib import pyplot as plt

filenames = []

for path in sys.argv[1:]:
    filenames.extend(glob.glob(path))

xlim = [1000,-1000]

bias_remap = False

for filename in filenames:

    with open(filename, 'r') as fp:
        raw = json.load(fp)

    label = raw.get('title', os.path.basename(filename))
    data = raw['data']
    data = list(filter(lambda x: x['valid'] != 0, data))

    def bias_map(x):
        return 1.037594*x + .04203

    xvals = [(x['bias_min']+x['bias_max'])/2 for x in data]
    xmin = [ x['bias_max'] for x in data]
    xmax = [ x['bias_max'] for x in data]
    if bias_remap:
        xvals = [bias_map(x) for x in xvals]
        xmin = [bias_map(x) for x in xmin]
        xmax = [bias_map(x) for x in xmax]

    xlim[0] = min(xlim[0], min(xmin))
    xlim[1] = max(xlim[1], max(xmax))

    xmin = [x-y for x,y in zip(xvals, xmin)]
    xmax = [x-y for x,y in zip(xvals, xmax)]

    yvals = [x['duration']*1000 for x in data]

    plt.scatter(xvals, yvals, s=2, label=label, alpha = 0.5)
    plt.errorbar(xvals, yvals, xerr=[xmin, xmax], fmt='None', zorder=-1, c='gray', elinewidth=1)

plt.title('Measured filter decay times')
if bias_remap:
    plt.xlabel('Bias Voltage (V)')
else:
    plt.xlabel('Unmapped Bias Voltage (V)')
plt.ylabel('Decay Time (ms)')
plt.xlim(*xlim)
plt.legend()
plt.grid(True)
ax = plt.gca()
ax.set_yscale('log')
plt.show()

