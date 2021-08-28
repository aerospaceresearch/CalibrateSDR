# Constants
RESAMPLE_FACTOR = 20
PSS_STEP = 9600
SEARCH_WINDOW = 150
PREAMBLE=30
AUX_BUFFER_SIZE = 20*1024


# variables
fs=1.92e6
fc=806e6
chan=0
gain=30
source=-1


def main():
    print("there is no gsm support in CalibrateSDR yet. If you know how to do it, please feel free to add it :)")
    print("or you can use Kalibrate-RTL from https://github.com/steve-m/kalibrate-rtl in the meantime")

if __name__ == '__main__':
    main()