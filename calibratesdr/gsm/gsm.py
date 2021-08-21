from calibratesdr.dabplus.dab import channels
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
from .arfcn_freq import channels, band_key
from .fcch_offset import calculate_offset


def wav_to_iq(file_path, from_index=2000, to_index=748000):
    """
    Input: file path towards IQ file as .wav
    Output: sample rate and array with memmap true
    """

    sample_rate, data = wavfile.read(file_path, True)
    samples = data[from_index:to_index, 0] + 1j * data[from_index:to_index, 1]

    return sample_rate, np.array(samples).astype("complex64") - (127.5 + 1j * 127.5)


def avg_power_spectrum(data, N=256, fs=1):
    """
    Input: array of IQ sample, N, sampling rate
    Output: average spectrum (using np.abs)
    """

    M = int(np.floor(len(data)/N))
    data_ = np.reshape(data[:M*N], (M, N)) * np.hamming(N)[None, :]
    X = np.fft.fftshift(np.fft.fft(data_, axis=1), axes=1)

    return np.r_[-N/2.0:N/2.0]/N*fs, np.mean(abs(X**2), axis=0)


def spectrogram_plot(t_range, f_range, y, dbf=60, fig=None):
    """
    Input --
    t_range: time axis, nt samples
    f_range: frequency axis, nf samples
    dbf: Dynamic range of the spectrum

    Output --
    Spectrogram, with xlabel Time in sec and ylabel Frequency in Hz
    """
    eps = 10.0**(-dbf/20.0)  # minimum signal
    y_max = abs(y).max()

    y_log = 20.0 * np.log10((abs(y) / y_max)*(1-eps) + eps)

    fig = plt.figure(figsize=(16, 6))
    plt.imshow(np.flipud(64.0*(y_log + dbf)/dbf), extent=t_range +
               f_range, cmap='RdYlBu', aspect='auto')
    plt.xlabel('Time, s')
    plt.ylabel('Frequency, Hz')
    plt.tight_layout()
    return fig


def spectrogram_hann(data, m, fs, fc, dbf=60, fig=None):
    """
    Split it into blocks of length m. 
    Function plots the spectrogram of x, calling function spectrogram_plot
    """
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
    plt.show()
    return None


def offset_plot(data, m, fs, fc=0):

    burst_t = 576.9e-6
    burst_len = 1 + fs*burst_t//1
    fcc = fc + 5000
    demod_data = np.exp(-1j * fcc * np.linspace(0, len(data), len(data)))*data

    spectrogram_hann(demod_data, m, fs, fcc)
    plt.show()

    h = signal.firwin(141, 7500, nyq=2400000.0/2, window='hanning')
    filtered_data = signal.fftconvolve(demod_data, h)[::10]
    spectrogram_hann(filtered_data, m, fs/10, fcc)
    plt.show()

    plt.figure(figsize=(16, 4))
    plt.plot(np.r_[0:len(filtered_data)]/fs*100, abs(filtered_data))
    plt.title('Magnitude of filtered and demodded signal')
    plt.xlabel('t [ms]')
    plt.show()


def gsm_plots(data, fs, fc=0):

    print(f"Sample rate used: {fs}")

    f, sp = avg_power_spectrum(data, N=256, fs=fs/1000)
    plt.figure(figsize=(8, 4))
    plt.plot(f, 10*np.log10(sp))
    plt.title('average power spectrum of GSM')
    plt.xlabel('frequency offset [KHz]')
    plt.show()

    plt.figure(figsize=(16, 4))
    plt.plot(np.r_[0:12000.0]/fs*1000, abs(data[:12000]))
    plt.title('Magnitude GSM signal, showing TDMA frames')
    plt.xlabel('t [ms]')
    plt.show()

    m = 128  # window length
    spectrogram_hann(data, m, fs, fc)
    plt.show()

    offset_plot(data, m, fs, fc=0)


def main(filepath=None, fc=0, sdr=False, input=input):

    fcc = (1625000.0 / 6.0) / 4.0
    h_bw = 15000

    if filepath != None:
        fs, data = wav_to_iq(filepath)
        # if input["gr"]== True
        gsm_plots(data, fs, fc)
        offset = calculate_offset(data, fs, fc)
        return (offset, offset / (fc + (1625000.0 / 6.0) / 4.0)*1e6)

    if sdr == True and input["fc"] != None:
        from rtlsdr import RtlSdr
        ppm = 1
        N_mf = 1  # debug
        device = input["rd"]
        sdr = RtlSdr(device_index=device)
        fs = 270833.002142  # debug
        fs = input["rs"]
        fc = input["fc"]  # debug
        gain = input["rg"]
        span = N_mf*235.4*.001
        ns = (span*fs+2048)//256 * 256
        print('Number of samples = ' + str(ns))

        sdr.sample_rate = fs
        sdr.gain = gain
        sdr.center_freq = fc
        sdr.set_freq_correction(ppm)
        data = sdr.read_samples(ns)[2048:]
        sdr.close()

        #gsm_plots(data, fs, fc)
        demod_data = np.exp(-1j * fcc * np.linspace(0,
                            len(data), len(data)))*data
        h = signal.firwin(141, h_bw/2, nyq=fs/2, window='hanning')
        filtered_data = signal.fftconvolve(demod_data, h)[::10]

        offset = calculate_offset(filtered_data, fcc, fs, graph=True)
        print(
            f"Offset Frequency: {offset} \nOffset in PPM: {offset / (fc + (1625000.0 / 6.0) / 4.0)*1e6}")

        # (offset, offset / (fc + (1625000.0 / 6.0) / 4.0)*1e6)

    if sdr == True and input["c"] != None:
        from rtlsdr import RtlSdr
        ppm = 1
        N_mf = 1  # debug
        fs = 270833.002142
        device = input["rd"]
        sdr = RtlSdr(device_index=device)
        sdr.sample_rate = fs
        sdr.gain = 20
        span = N_mf*235.4*.001
        ns = (span*fs+2048)//256 * 256

        #gsm_band = input("Enter band you would like to scan:  ")
        if input["c"] == "all":
            print("Enter one of the following as -c parameter\nGSM Bands: \n\t=>GSM_850\n\t=>GSM_R_900\n\t=>GSM_900\n\t=>GSM_E_900\n\t=>DCS_1800\n\t=>PCS_1900")

        gsm_freq = channels(band_key(input["c"]))

        for fc in gsm_freq:

            sdr.center_freq = fc
            sdr.set_freq_correction(ppm)
            data = sdr.read_samples(ns)[2048:]
            sdr.close()

            demod_data = np.exp(-1j * fcc * np.linspace(0,
                                                        len(data), len(data)))*data
            h = signal.firwin(141, h_bw/2, nyq=fs/2, window='hanning')
            filtered_data = signal.fftconvolve(demod_data, h)[::10]

            offset = calculate_offset(filtered_data, fcc, fs, graph=True)
            print(
                f"Offset Frequency: {offset} \nOffset in PPM: {offset / (fc + (1625000.0 / 6.0) / 4.0)*1e6}")


if __name__ == "__main__":
    main()
