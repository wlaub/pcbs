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

bias_remap = True
do_scale = True
do_offset = True
do_errorbars = False

sample_periods = []

for filename in filenames:

    with open(filename, 'r') as fp:
        raw = json.load(fp)

    scale = raw.get('scale', 1)
    offset = raw.get('offset', 0)
    label = raw.get('title', os.path.basename(filename))
    if do_scale:
        label = f'{label} ({1/scale:.3f})'
    if do_offset:
        label = f'{label} ({offset:.2f})'
    data = raw['data']
    data = list(filter(lambda x: x['valid'] != 0, data))



    def bias_map(x):
        return 1.037594*x + .04203

#    xvals = [(x['bias_min']+x['bias_max'])/2 for x in data]
    xvals = [x.get('bias_avg', (x['bias_min']+x['bias_max'])/2) for x in data]
    xmin = [ x['bias_max'] for x in data]
    xmax = [ x['bias_max'] for x in data]
    if bias_remap:
        xvals = [bias_map(x) for x in xvals]
        xmin = [bias_map(x) for x in xmin]
        xmax = [bias_map(x) for x in xmax]

    if do_offset:
        xvals = [x+offset for x in xvals]
        xmin = [x+offset for x in xmin]
        xmax = [x+offset for x in xmax]



    xlim[0] = min(xlim[0], min(xmin))
    xlim[1] = max(xlim[1], max(xmax))

    sample_periods.extend(list(set([x['sample_period'] for x in data])))

    xmin = [x-y for x,y in zip(xvals, xmin)]
    xmax = [x-y for x,y in zip(xvals, xmax)]

    yvals = [x['duration']*1000 for x in data]
    if do_scale:
        yvals = [x/scale for x in yvals]

    plt.scatter(xvals, yvals, s=2, label=label, alpha = 0.5)
    if do_errorbars:
        plt.errorbar(xvals, yvals, xerr=[xmin, xmax], fmt='None', zorder=-1, c='gray', elinewidth=1, alpha = 0.5)

#for ts in sample_periods:
#    plt.axhline(ts)

plt.title('Measured filter decay times')
xlabel = 'Bias Voltage (V)'
if do_offset:
    xlabel = 'Offset ' + xlabel
if not bias_remap:
    xlabel = 'Unmapped ' + xlabel
plt.xlabel(xlabel)
if do_scale:
    plt.ylabel('Normalized Decay Time (ms)')
else:
    plt.ylabel('Decay Time (ms)')
plt.xlim(*xlim)
plt.legend()
plt.grid(True)
ax = plt.gca()
ax.set_yscale('log')
plt.show()

