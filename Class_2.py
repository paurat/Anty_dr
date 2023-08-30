import numpy as np
from libhackrf import *
from pylab import *# for plotting
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
class SDR_radio(object,):
    def __init__(self, min_freq, max_freq, step_freq_size):
        self.min_freq=min_freq
        self.max_freq=max_freq
        self.step_freq_size=step_freq_size
    def get_max_min_freaq(self):
        return (self.min_freq, self.max_freq, self.step_freq_size)
    def set_max_freq(self, max_freq):
        self.max_freq= max_freq
    def set_min_freq(self, min_freq):
        self.min_freq= min_freq
    def set_step_freq_size(self, step_freq_size):
        self.step_freq_size= step_freq_size
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
        #while count_step<(max_freq-min_freq)/step_freq_size:
        hrf.sample_rate = step_freq_size
        hrf.center_freq = min_freq+step_freq_size*count_step+step_freq_size/2

        samples = hrf.read_samples(5e6)
        #print(count_step,hrf.center_freq)
        np.fft.fft(samples,None,-1,None)
        FFTSDR=np.abs(np.fft.rfft(samples,None,-1,None))
        FFTSDR=FFTSDR[1:]
        FFTSDR = np.average(FFTSDR.reshape(-1, 1000), axis=1)
        return (FFTSDR)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
       

       

        # plot data: x, y values
        self.graphWidget.plot(SDR.Freaq_read())


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
    SDR=SDR_radio(100e6,6000e6,5e6)
    # print(SDR.get_max_min_freaq())
    max=input("Введите максимальную частоту до 6000MГц  ")
    int_max=int(max)*1000000
    SDR.set_max_freq(int_max)
    min=input("Введите минимальную частоту от 100MГц  ")
    int_min=int(min)*1000000
    SDR.set_min_freq(int_min)
    step_freq_size=input("Введите шаг от 0,1MГц до 5MГц  ")
    int_step_freq_size=int(step_freq_size)*1000000
    SDR.set_step_freq_size(int_step_freq_size)
    # print(SDR.get_max_min_freaq())
    # print(SDR.Freaq_read())
    main()
    
