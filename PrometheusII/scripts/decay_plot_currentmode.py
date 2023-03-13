import time
import sys,os
import math
import json
import glob

import numpy as np
import scipy
import scipy.interpolate

from matplotlib import pyplot as plt
from matplotlib import widgets as mplwidgets

filenames = []
import pot_curve

for path in sys.argv[1:]:
    filenames.extend(glob.glob(path))


def es8_to_dmm(x):
    return 1.037594*x + .04203

bias_range = [0, -6.85]

def dmm_to_knob(x, dmm=bias_range):
#    dmm = [-4.76, -6.72]
#    dmm = [-4.76, -7.19]
    m = 1/(dmm[1]-dmm[0])
    b = -dmm[0]*m
    return m*x+b

#    return -0.4115226337*x-1.958847737

def parknob_to_knob(x, rt):
    if x >=1: return 1
    return -(math.sqrt(rt*rt+rt*(4*x*x-6*x+2) + (x-1)**2) +rt+x-1)/(2*(x-1))

knob_points = [
[0,0],
[.33, 1e2],
[.67, 2e3],
[1,10e3],
]

def get_interp_func(mbias=-6.6, tbias=-6.75):
    points = [
        [0,0],
        [mbias,.33],
        [tbias,.67],
        [-6.72, 1],
        ]
    interp = scipy.interpolate.interp1d(*zip(*points), bounds_error=False, fill_value='extrapolate')
    return interp
 
def dmm_to_piecewise(x, mbias=-6.6, tbias=-6.75):
    points = [
        [0,0],
        [mbias,.5],
        [tbias,1],
        ]
    interp = scipy.interpolate.interp1d(*zip(*points), bounds_error=False)
    return interp(x)


def dmm_to_log(x, B=-.216404, A=35185671051388.64):
    return (math.exp(x/B)-1)/A

bias_remap = True
do_scale = False
do_offset = True
do_errorbars = False

class DataSet():
    def __init__(self, filename):

        with open(filename, 'r') as fp:
            raw = self.raw = json.load(fp)

        data = raw['data']
        self.data = data = list(filter(lambda x: x['valid'] != 0, data))

        self.scale = raw.get('scale', 1)
        self.offset = raw.get('offset', 0)
        self.title = raw.get('title', os.path.basename(filename))
 
        self.xvals = [x.get('bias_avg', (x['bias_min']+x['bias_max'])/2) for x in data]
        self.xmin = [ x['bias_max'] for x in data]
        self.xmax = [ x['bias_max'] for x in data]

        self.yvals = [x['duration'] for x in data]

        self.fit_line()

    def fit_line(self):
        res = np.polyfit(self.xvals, [1/x for x in self.yvals], 1)
        self.slope, self.offset = res
        self.xoff = self.offset/self.slope 

        self.xoff = max(-min(self.xvals), self.xoff)

        self.timefunc = lambda x: 1/(x*self.slope)

    def plot(self, ax):
        kwargs = {
            's': 2,
            'alpha': 1
            }
      
        xmin = 1/(10*self.slope) 
        xvals = [xmin+3.3*x/10000 for x in range(10000)]
        yvals = [self.timefunc(x) for x in xvals] 
        ax.plot(xvals, yvals)

        kwargs['label'] = self.title
        ax.scatter([x + self.xoff for x in self.xvals], [y for y in self.yvals], **kwargs)


class PlotHandler():

    def __init__(self, datasets, targets):
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.datasets = datasets
        self.targets = targets

        self.param_defaults = {
            'scale': ['Scale', 0,1,1],
            'rt': ['Rt', 0,1,0],
            'rb': ['Rb',1e-6,1e-1,1e-3],
            'rtp': ['Rtp', 0,1,0],
            'rbp': ['Rbp', 0,1e-1,0],
            'gain': ['Gain',0, 1.5, 1],
            'offset': ['Offset', 0, .1, 0.0],
            'knee': ['Knee', 0,1,0.5],
            }
        self.active_params = ['rb', 'offset', 'gain', 'rt']
    
        self.sliders = {}
        self.params =[ { k:v[3] for k,v in self.param_defaults.items()} for x in datasets]
        gap = .08/len(self.active_params)
        for idx, key in enumerate(self.active_params):

            name, minval, maxval, defval = self.param_defaults[key]
            print(f'Registering {key} {name}')
            stagger = .01*(idx%2)
            sliderax = plt.axes([.92+gap*idx, .05+stagger, .01, .9-2*stagger])
            slider = mplwidgets.Slider(sliderax, name, 
                valmin = minval, valmax = maxval, valinit = defval,
                orientation='vertical'
                )
            slider.on_changed(lambda x, key=key: self.update_slider(key, x))
            self.sliders[key] = slider

        self.param_idx = 0
        self.buttons = []
        self.param_label = self.fig.text(.5, .98, self.datasets[0].title)

        for delta in [-1,1]:
            buttax = plt.axes([.5+(delta)*.025, .95, .05, .025])
            button = mplwidgets.Button(buttax, ['<','','>'][delta+1], )
            button.on_clicked(lambda x, dx=delta: self.update_param_idx(dx))
            self.buttons.append(button)

 
    def update_param_idx(self, delta):
        self.param_idx += delta
        count = len(self.datasets)
        if self.param_idx < 0: self.param_idx += count
        if self.param_idx >= count: self.param_idx -= count
        self.param_label.set_text(self.datasets[self.param_idx].title)
        for idx, key in enumerate(self.active_params):
            self.sliders[key].set_val(self.params[self.param_idx][key])

    def update_slider(self, key, val):
        oldval = self.params[self.param_idx][key]
        self.params[self.param_idx][key] = val
        if oldval != val:
            self.plot_all() 

    def plot_all(self):
        ax = self.ax

        pc = pot_curve.CurvedPot(res=100)
        ax.clear()

        pot = pot_curve.PotNetwork(res=100)

        res = 1000
        xknob = [x/res for x in range(1,res)]
        for idx, data in enumerate(self.datasets):
            rbp = self.params[idx]['rbp']
            rtp = self.params[idx]['rtp']
            rb = self.params[idx]['rb']
            rt = self.params[idx]['rt']
            offset = self.params[idx]['offset']
            knee = self.params[idx]['knee']
            gain = self.params[idx]['gain']
            def log_map(x):
                z = .1
                if x < 0.5:
                    return x*z*2
                else:
                    return z+(x-.5)*(1-z)/.5

#            xknob = [log_map(x) for x in xknob]
#            if rtp == 0:
#                vknob = [rb/(rb+x+rt) for x in vknob]
#            else:
#                vknob = [rb/(rb+1/(1/x+1/rtp)+rt) for x in vknob]

            pot.update(rt, rb, rtp, rbp, knee) 

#            bvknob = [3.3*x*gain for x in vknob]

            for ctol in [-.2, 0, .2]:
                for pottol in [-.2, 0, .2]:
                    pot.update(0, 0, rtp, rbp, knee) 
                    vknob = [rb/(rb+pot.rbot(x)*(1+pottol)+rt) for x in xknob]
                    vknob = [3.3*x*gain-offset for x in vknob]
                    yvals = [data.timefunc(x)*(1+ctol) for x in vknob]
                    ax.plot(xknob, yvals)

#            pot.update(rt, rb, rtp, rbp, knee) 
#            vknob = [pot.rbot(x)/(pot.rtop(x)+pot.rbot(x)) for x in xknob]
#            vknob = [3.3*x*gain for x in vknob]
#            yvals = [data.timefunc(x) for x in vknob]
#            ax.plot(xknob, yvals)




#        for data in self.datasets:
#            data.plot(ax)

        linestyle = {'linestyle':'--', 'c':'k', 'linewidth':1}
        ax.axhline(50e-3, **linestyle)
        ax.axhline(1, **linestyle)

        ax.set_title(f'')
        ax.set_ylabel('Decay time (s)')
#        ax.set_xlabel('Knob Position')
        ax.set_xlim(0,1)
        ax.set_ylim(1e-3, 10)
        ax.set_xlabel('Knob Position')
#        ax.set_xlabel(' ES-8 pre-attenuation control voltage (V)')
#        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.grid()
        ax.legend()

datasets = []

for filename in filenames:
    datasets.append(DataSet(filename))
    with open(filename, 'r') as fp:
        raw = json.load(fp)

handler = PlotHandler(datasets, knob_points)

handler.plot_all()
plt.show()

exit(0)

ax = plt.gca()

def plot_all_data(val):
    ax.clear()
    print(val)
    for data in datasets:
        data.reset_xvals()
        data.map_xvals(lambda x: x+data.offset)
        data.map_xvals(es8_to_dmm)
        data.map_xvals(dmm_to_log, B=val)

    for data in datasets:
        data.plot(ax)

    ax.plot(*zip(*knob_points), label='Knob Targets', c='k', linestyle='--', zorder=-1, linewidth=1)
    
    ax.set_xlim(0,1)
    ax.set_ylim(0, 10e3)
    ax.grid()
    
plot_all_data(-.216404)

sliderax = plt.axes([.91, .05, .01, .9])
slider = mplwidgets.Slider(sliderax, 'B', valmin=-.22, valmax=-.2, valinit=-.216, orientation='vertical')
slider.on_changed(plot_all_data)

ax.set_title('Measured filter decay times')
xlabel = 'Bias Voltage (V)'
if do_offset:
    xlabel = 'Offset ' + xlabel
if not bias_remap:
    xlabel = 'Unmapped ' + xlabel
ax.set_xlabel(xlabel)
if do_scale:
    ax.set_ylabel('Normalized Decay Time (ms)')
else:
    ax.set_ylabel('Decay Time (ms)')
ax.legend()
ax.grid(True)
#ax.set_yscale('log')
plt.show()

