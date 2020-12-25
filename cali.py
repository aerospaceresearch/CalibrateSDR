import argparse
import numpy as np
import os
import calibratesdr as cali

def load_data(filename, offset):
    samples = np.memmap(filename, offset=offset)
    return samples

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
                           help='scan with rtlsdr')
    my_parser.add_argument('-c',
                           action='store',
                           type=str,
                           help='scan by \"all\", by channel number \"0,1,...n\" or by blockname')
    my_parser.add_argument('-rs',
                           action='store',
                           type=int,
                           help='file/scan samplerate',
                           default=2048000)
    my_parser.add_argument('-rg',
                           action='store',
                           help='scan with gain',
                           default=20)
    my_parser.add_argument('-v',
                           '--verbose',
                           action='store_true',
                           help='an optional argument')

    # Execute parse_args()
    args = my_parser.parse_args()
    print(vars(args))
    input = vars(args)


    if input["f"] is not None:
        filename = input["f"]
        samplerate = input["rs"]
        mode = input["m"]

        if os.path.exists(filename):
            data = load_data(filename, offset=44)

            if mode == "dab":
                print("starting mode: dab")
                ppm = cali.dabplus.dab.get_ppm(data, samplerate = samplerate)
                print("your sdr's ppm is", ppm)

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

        #print(input["f"], input["rs"], input["m"])