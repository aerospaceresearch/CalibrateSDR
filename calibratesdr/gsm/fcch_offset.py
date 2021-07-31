import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
#from numpy.fft import *
from scipy import signal


def calculate_offset(data, fs, fc):
    num_taps = 51 # it helps to use an odd number of taps
    cut_off = 3000 # Hz
    sample_rate = 32000 # Hz

    # create our low pass filter
    h = signal.firwin(num_taps, cut_off, nyq=sample_rate/2)

    # plot the impulse response
    plt.plot(h, '.-')
    plt.show()
    return None