import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from numpy.fft import *
from matplotlib.pyplot import *
# from rtlsdr import RtlSdr
from scipy.io import wavfile


def wav_to_iq(file_path):
    sample_rate, data = wavfile.read(file_path, True)
    from_index = 2000
    to_index = 748000

    samples = data[from_index:to_index, 0] + 1j * data[from_index:to_index, 1]
    return sample_rate, np.array(samples).astype("complex64") - (127.5 + 1j * 127.5)


fs, data = wav_to_iq(
    "/home/jayaraj/Projects/calibratesdr_sdrtest/GSM/sdr-gsm-recordings/SDRSharp_20210327_124115Z_935800000Hz_IQ.wav")


def avg_power_spectrum(data, n=256, fs=1):
    M = int(floor(len(data) / n))
    x_ = reshape(data[:M * n], (M, n)) * np.hamming(n)[None, :]
    X = np.fft.fftshift(np.fft.fft(x_, axis=1), axes=1)

    return r_[-n / 2.0:n / 2.0] / n * fs, mean(abs(X ** 2), axis=0)



f, sp = avg_power_spectrum(data, n=1024, fs=fs)
fig = figure(figsize=(8,4))
plot(f,10*log10(sp))
title('average power spectrum of GSM')
xlabel('frequency offset [KHz]')
plt.show()

# plot
fig = figure(figsize=(16,4))
plot(r_[0:12000.0]/fs*1000,abs(data[:12000]))
title('Magnitude GSM signal, showing TDMA frames')
xlabel('t [ms]')
plt.show()

