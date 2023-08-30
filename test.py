import numpy as np
from libhackrf import *
from pylab import *# for plotting
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
while count_step<(max_freq-min_freq)/step_freq_size:
    hrf.sample_rate = step_freq_size
    hrf.center_freq = min_freq+step_freq_size*count_step+step_freq_size/2

    samples = hrf.read_samples(5e6)
    #print(count_step,hrf.center_freq)
    np.fft.fft(samples,None,-1,None)
    FFTSDR=np.abs(np.fft.rfft(samples,None,-1,None))
    FFTSDR=FFTSDR[1:]
    FFTSDR = np.average(FFTSDR.reshape(-1, 1000), axis=1)
    print(count_step)
    count_step +=1
    
