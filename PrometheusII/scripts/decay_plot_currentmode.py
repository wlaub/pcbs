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
 
        self.base_xvals = [x.get('bias_avg', (x['bias_min']+x['bias_max'])/2) for x in data]
        self.base_xmin = [ x['bias_max'] for x in data]
        self.base_xmax = [ x['bias_max'] for x in data]

        self.base_yvals = [x['duration']*1000 for x in data]
        self.yvals = self.base_yvals

        self.simple = False
        self.simplify()
        self.reset_xvals()

    def simplify(self):
        mixed = sorted(zip(self.base_yvals, self.base_xvals))
        chunks = []
        tchunk = []
        for y,x in mixed:
            if len(tchunk) == 0:
                tchunk.append([y,x])
            else:
                py = tchunk[-1][0]
                if y/py > 1.1 or abs(y-py) > 300:
                    chunks.append(tchunk)
                    tchunk = []
                tchunk.append([y,x])

        nxvals = []
        nyvals = []
        for chunk in chunks:
            oyvals, oxvals = zip(*chunk)
            nxvals.append(np.average(oxvals))
            nyvals.append(np.average(oyvals))

        self.base_simp_xvals = nxvals
        self.simp_yvals = nyvals
#        self.yvals =  self.base_yvals
        self.simple = True

    def reset_xvals(self):
        self.xvals = self.base_xvals
        self.xmin = self.base_xmin
        self.xmax = self.base_xmax
        if self.simple:
            self.simp_xvals = self.base_simp_xvals

    def map_xvals(self, func, *args, **kwargs):
        self.xvals = [func(x, *args, **kwargs) for x in self.xvals]
        self.xmin = [func(x, *args, **kwargs) for x in self.xmin]
        self.xmax = [func(x, *args, **kwargs) for x in self.xmax]
        if self.simple:
            self.simp_xvals = [func(x, *args, **kwargs) for x in self.simp_xvals]
 
    def plot(self, ax):
        kwargs = {
            's': 2,
            'alpha': 0.5
            }
        if not self.simple: kwargs['label'] = self.title
        ax.scatter(self.xvals, self.yvals, **kwargs)
        if self.simple:
            ax.plot(self.simp_xvals, self.simp_yvals, label=self.title, linewidth=1)

class PlotHandler():

    def __init__(self, datasets, targets):
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.datasets = datasets
        self.targets = targets

        B = -.216404
        A = 35185671051388.64
        mbias = -6.471
        tbias = -6.6448
        maxbias = bias_range[1]
        maxbias = -5.5

        self.param_defaults = {
            'scale': ['Scale', 0,1,1],
            'B': ['B', -.22, -.2, -.216404],
            'A': ['A', A*.5, A*2, A],
            'mbias': ['Mid', mbias-.1, mbias+.1, mbias],
            'tbias': ['Top', tbias-.1, tbias+.1, tbias],
            'rt': ['Rt', 0,.03, .0169],
            'rb': ['Rb', 0,1,0],
            'maxbias': ['Max\nBias', maxbias*1.05, maxbias*.95, maxbias ],
            'offset': ['Offset', 0, 1, 0],
            }
        self.active_params = ['rt', 'maxbias', 'offset']
    
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
        """
        for idx, data in enumerate(self.datasets):
            params = self.params[idx]
    
            data.reset_xvals()
            data.map_xvals(lambda x: x+params['offset'])
            data.map_xvals(es8_to_dmm)
#            data.map_xvals(dmm_to_log, B=self.B, A = self.A)
#            data.map_xvals(dmm_to_piecewise, self.mbias, self.tbias)
#            interp = get_interp_func(params['mbias'], params['tbias'])
#            data.map_xvals(interp)
#            data.map_xvals(lambda x: x/self.scale)

            pc.update(params['rt'], params['rb'])
            data.map_xvals(dmm_to_knob, [bias_range[0], params['maxbias']])
            data.map_xvals(pc.interp)


        for data in self.datasets:
            data.plot(ax)
        """

        for data in self.datasets:
            data.reset_xvals()
            data.map_xvals(lambda x: x)

            data.map_xvals(lambda x: x*0.03090785)
            data.map_xvals(lambda x: x*1000/10)
#            data.map_xvals(es8_to_dmm)
#            data.map_xvals(dmm_to_knob)
#            data.map_xvals(parknob_to_knob, .1)

        for data in self.datasets:
            data.yvals = [1/y for y in data.yvals]
            data.simp_yvals = [1/y for y in data.simp_yvals]
            data.plot(ax)



#        ax.plot(*zip(*self.targets), label='Knob Targets', c='k', linestyle='--', zorder=-1, linewidth=1)

#        ax.axhline(1000, linestyle='--', linewidth=0.5, c='k')
#        ax.axvline(.95, linestyle='--', linewidth=2, c='k')
        
        ax.set_title(f'Knob to Decay Time, bias range {bias_range[0]:.2f} to {self.params[0]["maxbias"]:.3f} V')
        ax.set_ylabel('Inverse decay time (kHz)')
#        ax.set_xlabel('Knob Position')
#        ax.set_xlim(0,1)
#        ax.set_ylim(0, 15e3)
        ax.set_xlabel(' ES-8 pre-attenuation control voltage (V)')
#        ax.set_yscale('log')
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

