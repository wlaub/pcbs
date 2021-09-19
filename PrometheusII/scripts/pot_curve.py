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

class CurvedPot():
    def __init__(self, res = 1000):
        self.res = res

    def par(self, a, b):
        if a == 0 or b == 0: return 0
        return 1/(1/a+1/b)

    def map_value(self, x):

        rt = 1-x
        if self.top:
            rt = self.par(rt, self.top)

        rb = x
        if self.bot:
            rb = self.par(rb, self.bot)

        return rb/(rb+rt)

    def update(self, rt, rb):
        res = self.res
        self.top = rt
        self.bot = rb
        self.xvals = xvals = [x/res for x in range(res)]
        self.yvals = yvals = [self.map_value(x) for x in xvals] 

        interp = scipy.interpolate.interp1d(
            yvals, xvals,
            bounds_error=False, 
            fill_value='extrapolate'
            )
        self.interp = interp


class PlotHandler():

    def get_sliderax(self, idx):
        return plt.axes([.91+.04*idx, .06, .01, .9])

    def __init__(self):
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax


        self.top = 0
        self.bot = 0.015

        """
        sliderax = self.get_sliderax(0)
        self.top_slider = mplwidgets.Slider(sliderax, 'Top',
                valmin = 0,
                valmax = 1,
                valinit = self.top,
                orientation='vertical',
                )
        self.top_slider.on_changed(self.update_top)
        """

        sliderax = self.get_sliderax(0.5)
        self.bot_slider = mplwidgets.Slider(sliderax, 'Bot',
                valmin = 0,
                valmax =.01,
                valinit = self.bot,
                orientation='vertical',
                )
        self.bot_slider.on_changed(self.update_bot)


    def update_top(self, val):
        self.top = val
        self.plot_all()

    def update_bot(self, val):
        self.bot = val
        self.plot_all()

    def plot_all(self):
        ax = self.ax
        
        ax.clear()

        pc = CurvedPot()
        pc.update(self.top, self.bot)
        xvals = pc.xvals
        yvals = pc.yvals    

#        xvals = [x/1000 for x in range(1000)]
#        yvals = [pc.interp(x) for x in xvals]
   

        ax.axhline(10e-3, linestyle = '--', c='k')
        ax.axvline(.95, linestyle='--', c='k')


        vcctol = 0.1
        pottol = 0.2

        vcc = [3.3*(1-vcctol), 3.3, 3.3*(1+vcctol)]
        rtol = [1-pottol, 1, 1+pottol]
        labels = ['Minimum', 'Nominal', 'Maximum']

        for idx in range(3):
            pc.update(self.top, self.bot*rtol[idx])
            xvals = pc.xvals
            yvals = pc.yvals    
            tyvals = [y*vcc[idx] for y in yvals]
            ax.plot(xvals, tyvals, linewidth=1, label=labels[idx])

        ax.set_title(f'VCC Tolerance: {vcctol:.1%} | Pot Tolerance: {pottol:.1%}')

        ax.set_ylabel('Knob Output (V)')
        ax.set_xlabel('Knob Position')
        ax.set_xlim(0,1)
        ax.set_ylim(0,.1)
        ax.grid()
        ax.legend()


if __name__ == '__main__':
    handler = PlotHandler()

    handler.plot_all()
    plt.show()


