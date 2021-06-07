import numpy as np
from scipy.fftpack import fft, fftshift, ifft
import matplotlib.pyplot as plt
import calibratesdr as cali
from rtlsdr.helpers import limit_calls


def movingaverage(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'same')
    return sma


def reduce_outliers(dif):

    limit_b4 = 0.0
    limit_set = 1.0
    std_factor = 3.0
    counter = 0

    while limit_b4 - np.std(dif) * std_factor != 0 and \
            limit_set < np.std(dif) * std_factor and \
            counter < 20 and np.std(dif) != 0:

        std = np.std(dif)
        meany = np.mean(dif)

        limit = std * std_factor

        for j in range(len(dif)):

            if np.abs(dif[j] - meany) >= limit:
                #print("pop", counter, j, np.abs(dif[j] - meany), limit)
                dif = np.delete(dif, j)
                break

        limit_b4 = limit
        counter += 1

    return dif


def load_data(filename, offset):
    samples = np.memmap(filename, offset=offset)
    return samples


def signal_bar(snr, snr_max):
    bar_length = 20

    if snr_max != 0:
        percent = snr / snr_max
    else:
        percent = 0.0

    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))

    bar = "[{0}] {1}%".format(hashes + spaces, int(round(percent * 100)))

    return bar


def get_fft(data, samplerate=2048000):
    adc_offset = -127

    signal_fft = []
    window = samplerate

    for slice in range(0, int(len(data) // (window * 2)) * window * 2, window * 2):
        data_slice = (adc_offset + data[slice: slice + window * 2: 2]) +\
            1j * (adc_offset + data[slice + 1: slice + window * 2: 2])

        norm_fft = (1.0 / window) * fftshift(fft(data_slice))
        abs_fft = np.abs(norm_fft)

        transform = 10 * np.log10(abs_fft / np.abs(adc_offset))

        signal_fft.append(transform)

    return signal_fft


def record_with_rtlsdr(sdr, rs, cf, ns, rg, filename):

    sdr.rs = rs
    sdr.fc = cf
    sdr.gain = rg

    f = open(filename, 'wb')

    BLOCK_SIZE = 2**20

    @limit_calls(ns * 2 / BLOCK_SIZE)
    def callback(data, context):
        f.write(data)

    sdr.read_bytes_async(callback, BLOCK_SIZE)
    f.close()


def scan_one_dab_channel(dabchannels, channel, sdr, rs, ns, rg, filename, samplerate, show_graph, verbose):

    cf = dabchannels["dab"][channel]["f_center"]
    block = dabchannels["dab"][channel]["block"]

    record_with_rtlsdr(sdr, rs, cf, ns, rg, filename)

    data = load_data(filename, offset=0)
    dab_ppm = cali.dabplus.dab.get_ppm(
        data, samplerate=samplerate, show_graph=show_graph, verbose=verbose)

    dab_signal_fft = get_fft(data, samplerate=samplerate)

    dab_signal_fft_mean = np.mean(dab_signal_fft, axis=0)
    dab_signal_bins = cali.dabplus.dab.signal_level(dab_signal_fft_mean, 200)
    dab_snr = cali.dabplus.dab.signal_dynamics(dab_signal_bins, 12)

    if show_graph == True:
        plt.plot(dab_signal_bins)
        plt.grid()
        plt.title("dab block shape")
        plt.xlabel("sample bin")
        plt.ylabel("amplitude")
        plt.show()

    limit_db = 2.0
    dab_block_detected = cali.dabplus.dab.block_check(
        dab_signal_bins, dab_snr, limit_db=limit_db)

    del data

    return channel, block, cf, dab_snr, dab_block_detected, dab_ppm
