import argparse
import numpy as np
import os
from scipy.fftpack import fft, fftshift, ifft
from tqdm import tqdm
import time
import calibratesdr as cali


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


def get_fft(data, samplerate = 2048000):
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

    samples = sdr.read_bytes(ns * 2)

    f = open(filename, 'wb')
    f.write(samples)
    f.close()

    return samples

def main(input):

    print("let's find your SDR's oscillator precision")

    show_graph = input["graph"]
    verbose = input["verbose"]

    samplerate = input["rs"]
    mode = input["m"]

    if input["f"] is not None:
        print("loading file...")

        filename = input["f"]

        if os.path.exists(filename):
            data = load_data(filename, offset=44)

            if mode == "dab":
                print("starting mode: dab")
                ppm = cali.dabplus.dab.get_ppm(data, samplerate=samplerate, show_graph=show_graph, verbose=verbose)
                print("your sdr's precision is", ppm, "ppm")

            elif mode == "dvbt":
                print("starting mode: dvbt")
                cali.dvbt.dvbt.main()

            elif mode == "gsm":
                print("starting mode: gsm")
                cali.gsm.gsm.main()

            else:
                print("ending")

        else:
            print("sorry, file not found. try again.")


    elif input["s"] is not None:
        # scanning with your sdr

        print("scanning...")

        if mode == "dab":
            print("starting mode: dab")

            from rtlsdr import RtlSdr
            filename = "tmp.dat"
            device = input["rd"]
            sdr = RtlSdr(device_index=device)
            rs = input["rs"]
            rg = input["rg"]
            ns = rs * input["nsec"] #seconds
            c = input["c"]

            result = []

            dabchannels = cali.dabplus.dab.channels()

            if c == "all":
                print("Scanning all channels")


                for channel in tqdm(range(len(dabchannels["dab"])),
                                    desc="Scanning…",
                                    ascii=False,
                                    ncols=75):

                    cf = dabchannels["dab"][channel]["f_center"]
                    block = dabchannels["dab"][channel]["block"]

                    record_with_rtlsdr(sdr, rs, cf, ns, rg, filename)

                    data = load_data(filename, offset=0)
                    dab_ppm = cali.dabplus.dab.get_ppm(data, samplerate=samplerate, show_graph=show_graph, verbose=verbose)

                    dab_signal_fft = get_fft(data, samplerate=samplerate)

                    dab_signal_fft_mean = np.mean(dab_signal_fft, axis=0)
                    dab_signal_bins = cali.dabplus.dab.signal_level(dab_signal_fft_mean, 200)
                    dab_snr = cali.dabplus.dab.signal_dynamics(dab_signal_bins, 12)
                    limit_db = 2.0
                    dab_block_detected = cali.dabplus.dab.block_check(dab_signal_bins, dab_snr, limit_db=limit_db)


                    result.append([channel, block, cf, dab_snr, dab_block_detected, dab_ppm])

                    del data

            else:
                print("Scanning only channel #", c)

                channel = int(c)
                cf = dabchannels["dab"][channel]["f_center"]
                block = dabchannels["dab"][channel]["block"]

                record_with_rtlsdr(sdr, rs, cf, ns, rg, filename)

                data = load_data(filename, offset=0)
                dab_ppm = cali.dabplus.dab.get_ppm(data, samplerate=samplerate, show_graph=show_graph, verbose=verbose)

                dab_signal_fft = get_fft(data, samplerate=samplerate)

                dab_signal_fft_mean = np.mean(dab_signal_fft, axis=0)
                dab_signal_bins = cali.dabplus.dab.signal_level(dab_signal_fft_mean, 200)
                dab_snr = cali.dabplus.dab.signal_dynamics(dab_signal_bins, 12)
                limit_db = 2.0
                dab_block_detected = cali.dabplus.dab.block_check(dab_signal_bins, dab_snr, limit_db=limit_db)


                result.append([channel, block, cf, dab_snr, dab_block_detected, dab_ppm])

                del data


            # output
            dab_snr_max = 0
            for i in range(len(result)):
                if i == 0 or dab_snr_max < result[i][3]:
                    dab_snr_max = result[i][3]


            print("")
            print("____Results_______________________________________________________________________________________")
            print("#   , block, freq [Hz], SNR [dB] , Prec. [ppm], offset [Hz], block [x][o][ ] & signal strength")
            print("--------------------------------------------------------------------------------------------------")
            for i in range(len(result)):
                channel = result[i][0]
                block = result[i][1]
                cf = result[i][2]
                dab_snr = result[i][3]

                dab_block_detected = "[ ]"
                if result[i][4] == 1:
                    dab_block_detected = "[o]"
                elif result[i][4] == 2:
                    dab_block_detected = "[x]"

                dab_ppm = result[i][5]

                bar = signal_bar(dab_snr, dab_snr_max)
                #print(channel, block, cf, dab_snr, dab_ppm, dab_block_detected, bar)
                f_offset = 0.0

                if dab_ppm != None:
                    f_offset = cf / 1000000.0 * dab_ppm

                    print("# {0:2d}, {1:5s}, {2:9.0f}, {3:+9.5f}, {4:+10.4f}, {5:11.1f}, {6:4s} {7}".
                          format(channel, block, cf, dab_snr, dab_ppm, f_offset, dab_block_detected, bar))
                else:

                    print("# {0:2d}, {1:5s}, {2:9.0f}, {3:+9.5f},       None, {5:11.1f}, {6:4s} {7}".
                          format(channel, block, cf, dab_snr, dab_ppm, f_offset, dab_block_detected, bar))

            sdr.close()

        elif mode == "dvbt":
            print("starting mode: dvbt")
            cali.dvbt.dvbt.main()

        elif mode == "gsm":
            print("starting mode: gsm")
            cali.gsm.gsm.main()

        else:
            print("ending")


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser()

    my_parser.add_argument('-f',
                           action='store',
                           type=str,
                           help='select path to input file')
    my_parser.add_argument('-m',
                           action='store',
                           choices=['dab', 'dvbt', 'gsm'],
                           help='select mode',
                           default='dab')
    my_parser.add_argument('-s',
                           action='store',
                           choices=['rtlsdr'],
                           help='scan with rtlsdr',
                           default='rtlsdr')
    my_parser.add_argument('-c',
                           action='store',
                           type=str,
                           help='scan by \"all\" channels, by channel number \"0,1,...n\" or by blockname',
                           default = 'all')
    my_parser.add_argument('-rs',
                           action='store',
                           type=int,
                           help='file/scan samplerate',
                           default=2048000)
    my_parser.add_argument('-rg',
                           action='store',
                           type=int,
                           help='scan with gain',
                           default=20)
    my_parser.add_argument('-rd',
                           action='store',
                           type=int,
                           help='scan with device',
                           default=0)
    my_parser.add_argument('-nsec',
                           action='store',
                           type=float,
                           help='scan for n-seconds',
                           default=10)
    my_parser.add_argument('-gr',
                           '--graph',
                           action='store_true',
                           help='activate graphs',
                           default=False)
    my_parser.add_argument('-v',
                           '--verbose',
                           action='store_true',
                           help='an optional argument')

    # Execute parse_args()
    args = my_parser.parse_args()
    print(vars(args))

    main(vars(args))