import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal


def burst_find(data, fs):
    
    burst_time = 576.9e-6 #seconds
    half_len = fs*burst_time//2 + 3

    normed = (abs(data)/max(abs(data)))**2
    normed[normed < 0.5] = 0
    
    pulses = []
    for i in range(len(normed)-2):
        if normed[i+1]>normed[i] and normed[i+1]>normed[i+2]:
            if(i-half_len < 0 or i+half_len >= len(normed)-2):
                continue
            else:
                pulses += [(i+1-half_len, i+1+half_len)]

    return np.array(pulses).astype(int)



def calculate_offset(data, fcc, fs, graph=True):

    L = fs/10 # for fft res = 10 Hz
    burst_pos = burst_find(data,fs/10)
    
    ffts = []
    for i in range(len(burst_pos)):
        ffts += [np.fft.fft(np.append(data[burst_pos[i][0]:burst_pos[i][1]], np.zeros(int(L)-(burst_pos[i][1]-burst_pos[i][0]))))]
    mean_power = np.mean(np.fft.fftshift(abs(np.array(ffts)))**2, axis=0)
    idx = np.argmax(mean_power)
    fcch = idx*(fs/L)
    
    if graph:
        plt.figure()
        plt.plot(mean_power)
        plt.title('Average power spectrum of DFTs')
        plt.xlabel('Frequency Offset [KHz]')
        plt.show()
   
    return (fcch) - (1625000.0 / 6.0) / 4.0
