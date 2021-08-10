import argparse
import os
from tqdm import tqdm
import time
import calibratesdr as cali


def get_gsm(input, sdr=True):
    
    from rtlsdr import RtlSdr
    filename = "tmp.dat"
    device = input["rd"]
    sdr = RtlSdr(device_index=device)
    rs = input["rs"]
    rg = input["rg"]
    ns = rs * input["nsec"]  # seconds
    c = input["c"]

    result = []

    dabchannels = cali.dabplus.dab.channels()

    if c == "all":
        print("Scanning all channels")

        for channel in tqdm(range(len(dabchannels["dab"])),
                            desc="Scanning…",
                            ascii=False,
                            ncols=75):
            channel, block, cf, dab_snr, dab_block_detected, dab_ppm = \
                cali.utils.scan_one_dab_channel(dabchannels, channel, sdr, rs, ns, rg, filename, samplerate,
                                                show_graph, verbose)

            result.append([channel, block, cf, dab_snr,
                            dab_block_detected, dab_ppm])

    else:
        print("Scanning only channel #", c)

        channel = int(c)
        channel, block, cf, dab_snr, dab_block_detected, dab_ppm = \
            cali.utils.scan_one_dab_channel(dabchannels, channel, sdr, rs, ns, rg, filename, samplerate,
                                            show_graph, verbose)

        result.append([channel, block, cf, dab_snr,
                        dab_block_detected, dab_ppm])

    # output
    dab_snr_max = 0
    for i in range(len(result)):
        if i == 0 or dab_snr_max < result[i][3]:
            dab_snr_max = result[i][3]

    print("")
    print("____Results_______________________________________________________________________________________")
    print(
        "#   , block, freq [Hz], SNR [dB] , Prec. [ppm], offset [Hz], block [x][o][ ] & signal strength")
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

        bar = cali.utils.signal_bar(dab_snr, dab_snr_max)

        f_offset = 0.0

        if dab_ppm != None:
            f_offset = cf / 1000000.0 * dab_ppm

            print("# {0:2d}, {1:5s}, {2:9.0f}, {3:+9.5f}, {4:+10.4f}, {5:+11.1f}, {6:4s} {7}".
                    format(channel, block, cf, dab_snr, dab_ppm, f_offset, dab_block_detected, bar))
        else:

            print("# {0:2d}, {1:5s}, {2:9.0f}, {3:+9.5f},       None, {5:+11.1f}, {6:4s} {7}".
                    format(channel, block, cf, dab_snr, dab_ppm, f_offset, dab_block_detected, bar))

    sdr.close()
