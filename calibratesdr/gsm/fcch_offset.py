import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
#from numpy.fft import *
from scipy import signal


def wav_to_iq(file_path, from_index=2000, to_index=748000):

    sample_rate, data = wavfile.read(file_path, True)
    samples = data[from_index:to_index, 0] + 1j * data[from_index:to_index, 1]

    return sample_rate, np.array(samples).astype("complex64") - (127.5 + 1j * 127.5)


def avg_power_spectrum(data, N=256, fs=1):

    M = int(np.floor(len(data)/N))
    data_ = np.reshape(data[:M*N], (M, N)) * np.hamming(N)[None, :]
    X = np.fft.fftshift(np.fft.fft(data_, axis=1), axes=1)

    return np.r_[-N/2.0:N/2.0]/N*fs, np.mean(abs(X**2), axis=0)


def spectrogram_plot(t_range, f_range, y, dbf=60, fig=None):

    eps = 10.0**(-dbf/20.0)  # minimum signal
    y_max = abs(y).max()

    y_log = 20.0 * np.log10((abs(y) / y_max)*(1-eps) + eps)
    #img = 256*(y_log + dbf)/dbf - 1

    fig = plt.figure(figsize=(16, 6))
    plt.imshow(np.flipud(64.0*(y_log + dbf)/dbf), extent=t_range +
               f_range, cmap='RdYlBu', aspect='auto')
    plt.xlabel('Time, s')
    plt.ylabel('Frequency, Hz')
    plt.tight_layout()
    return fig


def spectrogram_hann(data, m, fs, fc, dbf=60, fig=None):

    isreal_bool = np.isreal(data).all()
    # print(isreal_bool)

    length = len(data)
    nt = (length + m - 1) // m
    data = np.append(data, np.zeros(-length+nt*m))
    data = data.reshape((m//2, nt*2), order='F')
    data = np.concatenate((data, data), axis=0)
    data = data.reshape((m*nt*2, 1), order='F')
    data = data[np.r_[m//2:len(data), np.ones(m//2)*(len(data)-1)
                      ].astype(int)].reshape((m, nt*2), order='F')

    xmw = data * np.hanning(m)[:, None]

    # frequency index
    t_range = [0.0, length / fs]

    if isreal_bool:
        f_range = [fc, fs / 2.0 + fc]
        xmf = np.fft.fft(xmw, len(xmw), axis=0)
        fig = spectrogram_plot(t_range, f_range, xmf[0:m//2, :], dbf, fig)
    else:
        f_range = [-fs / 2.0 + fc, fs / 2.0 + fc]
        xmf = abs(np.fft.fftshift(np.fft.fft(xmw, len(xmw), axis=0), axes=0))
        fig = spectrogram_plot(t_range, f_range, xmf, dbf, fig)

    return fig


def gsm_plots(filepath=None, fc=0):

    
    #filepath = "/home/jayaraj/Projects/calibratesdr_sdrtest/GSM/sdr-gsm-recordings/SDRSharp_20210327_124115Z_935800000Hz_IQ.wav"
    
    if filepath==None:
        print("No filepath specified, please retry giving -filepath argument")
        
    

    fs, data = wav_to_iq(filepath)
    print(f"Sample rate used: {fs}")
    
    f, sp = avg_power_spectrum(data, N=256, fs=fs/1000)
    plt.figure(figsize=(8, 4))
    plt.plot(f, 10*np.log10(sp))
    plt.title('average power spectrum of GSM')
    plt.xlabel('frequency offset [KHz]')
    plt.show()

    # plot
    plt.figure(figsize=(16, 4))
    plt.plot(np.r_[0:12000.0]/fs*1000, abs(data[:12000]))
    plt.title('Magnitude GSM signal, showing TDMA frames')
    plt.xlabel('t [ms]')
    plt.show()

    m = 500  # window length
    spectrogram_hann(data, m, fs, fc)
    plt.show()


if __name__ == "__main__":
    gsm_plots()