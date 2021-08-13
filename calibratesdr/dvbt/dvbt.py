import numpy as np
import matplotlib.pyplot as plt
import calibratesdr as cali
from dsp import *
# import scipy.signal as signal
# from scipy.fftpack import fft,fftfreq

def show_graph():
    plt.specgram(data, NFFT=1024, Fs=samplerate)
    plt.title("PSD of 'signal' loaded from file")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.show()

    #power spectral density
    plt.psd(data, NFFT=1024, Fs=samplerate)
    plt.title("PSD of 'signal' loaded from file")
    plt.show() 


def get_ppm(data, samplerate, show_graph = False, verbose = False):
	# frequency offset calculation
    iq_data = data[0::2] + 1j*data[1::2]
    
    data_carriers, super_frame_start = run_dsp(iq_data)

    ppm = offset(data_carriers, super_frame_start)

    if show_graph == True:
        show_graph(data,samplerate)

    # if mode == '2':
    #     print("2K mode")
    #     # for 2k mode 

    # elif mode == '8':
    #     print("8K mode")
    #     # for 8k mode

    # print("We are working on it.")
    return ppm

def main():
    # print("there is no dvbt support in CalibrateSDR yet. If you know how to do it, please feel free to add it :)")
    # print("with time, we will look into what these _pilote-tones_ are doing and if we could use them.")
    print(" This is the DVB-T support so far available.")


if __name__ == '__main__':
    main()
