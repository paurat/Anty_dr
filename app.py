import numpy as np
from libhackrf import *
from pylab import *     # for plotting
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

hrf = HackRF()

# Переменные частоты
min_freq=100e6
max_freq=6000e6
step_freq_size=5e6 #от 0,1 МГц до 5МГц

# Счетчики
count_mode=0
count_step=0

# Усилители
#hrf.enable_amp()
hrf.disable_amp()
hrf.lna_gain = 8
hrf.vga_gain = 22
hrf.sample_rate = step_freq_size
hrf.center_freq = min_freq+step_freq_size*count_step+step_freq_size/2

samples = hrf.read_samples(10e6)
#print(count_step,hrf.center_freq)
FFTSDR=np.abs(np.fft.rfft(samples,None,-1,None))
FFTSDR=FFTSDR[1:]
FFTSDR = np.average(FFTSDR.reshape(-1, 1000), axis=1)
print(FFTSDR[:100])

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

       

        # plot data: x, y values
        self.graphWidget.plot(FFTSDR)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
    