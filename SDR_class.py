import numpy as np
from libhackrf import *
from pylab import *# for plotting
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class SDR_read(object,):
    def __init__(self, min_freq, max_freq, step_freq_size):
        self.min_freq=min_freq
        self.max_freq=max_freq
        self.step_freq_size=step_freq_size
    def Freaq_read(self):
        hrf = HackRF()
        min_freq=self.min_freq
        max_freq=self.max_freq
        step_freq_size=self.step_freq_size #от 0,1 МГц до 5МГц
        # Счетчики
        count_mode=0
        count_step=0
        # Усилители
        #hrf.enable_amp()
        hrf.disable_amp()
        hrf.lna_gain = 8
        hrf.vga_gain = 22
        while count_step<(max_freq-min_freq)/step_freq_size:
            hrf.sample_rate = step_freq_size
            hrf.center_freq = min_freq+step_freq_size*count_step+step_freq_size/2

            samples = hrf.read_samples(5e6)
            #print(count_step,hrf.center_freq)
            np.fft.fft(samples,None,-1,None)
            FFTSDR=np.abs(np.fft.rfft(samples,None,-1,None))
            FFTSDR=FFTSDR[1:]
            FFTSDR = np.average(FFTSDR.reshape(-1, 1000), axis=1)
            count_step +=1
            print(count_step)
            return "count is %s, %s, %s"  % (count_step,self.min_freq, self.step_freq_size)
if __name__ == "__main__":

    SDR=SDR_read(100e6,6000e6,5e6)
    print(SDR.Freaq_read())
