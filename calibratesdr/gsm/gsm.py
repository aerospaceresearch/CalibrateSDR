import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from numpy.fft import *
from matplotlib.pyplot import *
#from rtlsdr import RtlSdr
from scipy.io import wavfile


def packed_bytes_to_iq(file_path):
    sample_rate, iq_data = wavfile.read(file_path, mmap=True)

    iq_data = np.ctypeslib.as_array(iq_data[2000:74800])
    iq_data = iq_data.astype(np.float64).view(np.complex128)

    iq_data /= 127.5
    iq_data -= (1 + 1j)

    return sample_rate, iq_data.reshape(len(iq_data))


def avg_power_spectrum(x, N=256, fs=1):
    M = int(floor(len(x) / N))
    x_ = reshape(x[:M * N], (M, N)) * np.hamming(N)[None, :]
    X = np.fft.fftshift(np.fft.fft(x_, axis=1), axes=1)

    return r_[-N / 2.0:N / 2.0] / N * fs, mean(abs(X ** 2), axis=0)


def spectrogram_plot(t_range, f_range, y, dbf=60, fig=None):
    eps = 10.0 ** (-dbf / 20.0)  # minimum signal

    # find maximum
    y_max = abs(y).max()

    # compute 20*log magnitude, scaled to the max
    y_log = 20.0 * np.log10((abs(y) / y_max) * (1 - eps) + eps)

    # rescale image intensity to 256
    img = 256 * (y_log + dbf) / dbf - 1

    fig = figure(figsize=(16, 6))

    plt.imshow(np.flipud(64.0 * (y_log + dbf) / dbf),
               extent=t_range + f_range, cmap=plt.cm.gray, aspect='auto')
    plt.xlabel('Time, s')
    plt.ylabel('Frequency, Hz')
    plt.tight_layout()


def spectrogram_hann_ovlp(x, m, fs, fc, dbf=60, fig=None):
    # check if x is real
    isreal_bool = isreal(x).all()

    lx = len(x)
    nt = (lx + m - 1) // m
    x = append(x, zeros(-lx + nt * m))
    x = x.reshape((m // 2, nt * 2), order='F')
    x = concatenate((x, x), axis=0)
    x = x.reshape((m * nt * 2, 1), order='F')
    x = x[r_[m // 2:len(x), ones(m // 2) * (len(x) - 1)
             ].astype(int)].reshape((m, nt * 2), order='F')

    xmw = x * hanning(m)[:, None]

    # frequency index
    t_range = [0.0, lx / fs]

    if isreal_bool:
        f_range = [fc, fs / 2.0 + fc]
        xmf = fft(xmw, len(xmw), axis=0)
        fig = spectrogram_plot(t_range, f_range, xmf[0:m // 2, :], dbf, fig)
    else:
        f_range = [-fs / 2.0 + fc, fs / 2.0 + fc]
        xmf = abs(fftshift(fft(xmw, len(xmw), axis=0), axes=0))
        fig = spectrogram_plot(t_range, f_range, xmf, dbf, fig)

    return fig


def main(filepath, fc):

    fs, data = packed_bytes_to_iq(filepath)
    print(f"Sample rate used: {fs}")

    # Usage of Pyrtlsdr API - pending work [Just written for note]

    # sdr = RtlSdr()
    # sdr.sample_rate = fs
    # sdr.gain = gain
    # sdr.center_freq = fc
    # sdr.set_freq_correction(ppm)
    # data = sdr.read_samples(25600*3)[2000:] #first 2000 samples are not good
    # sdr.close()

    # compute average power spectrum
    f, sp = avg_power_spectrum(data, N=256, fs=fs / 1000)

    fig = figure(figsize=(8, 4))
    plot(f, 10 * log10(sp))
    title('average power spectrum of GSM')
    xlabel('frequency offset [KHz]')
    plt.show()

    # plot of TDMA frames
    fig = figure(figsize=(16, 4))
    plot(r_[0:12000.0] / fs * 1000, abs(data[:12000]))
    title('Magnitude GSM signal, showing TDMA frames')
    xlabel('t [ms]')
    plt.show()

    spectrogram_hann_ovlp(data, 156, fs, fc, dbf=60)
    plt.show()

    # Simple specgram
    plt.specgram(data, NFFT=256, Fs=fs)
    plt.title("Power spectral density of signal")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.show()

    # plt.psd(data, NFFT=256, Fs=fs)
    # plt.title("PSD of 'signal' loaded from file")
    # plt.show()

# def main():
#     print("there is no gsm support in CalibrateSDR yet. If you know how to do it, please feel free to add it :)")
#     print("or you can use Kalibrate-RTL from https://github.com/steve-m/kalibrate-rtl in the meantime")

# if __name__ == '__main__':
#     main()
