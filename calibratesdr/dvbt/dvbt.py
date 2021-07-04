import numpy as np
import matplotlib.pyplot as plt
import calibratesdr as cali
import scipy.signal as signal
from scipy.fftpack import fft,fftfreq
import os

filename = input("Enter the filename")

dat = np.fromfile(filename, 'float32')

# Converting to IQ complex
dat = dat[0::2] + 1j*dat[1::2]

plt.specgram(dat, NFFT=1024, Fs=1000000)
plt.title("PSD of 'signal' loaded from file")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.show()

def get_ppm(data, samplerate, show_graph = False, verbose = False):
	# frequency offset calculation
    print("We are working on it.")

# def main():
#     print("there is no dvbt support in CalibrateSDR yet. If you know how to do it, please feel free to add it :)")
#     print("with time, we will look into what these _pilote-tones_ are doing and if we could use them.")

if __name__ == '__main__':
    main()
