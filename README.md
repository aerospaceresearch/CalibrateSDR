# CalibrateSDR
## what’s my frequency?

### How to build project?
1. Clone the repo
2. Run cali.py
3. Make sure you have all the required libs (check requirements.txt)

### Basic commands
python.exe cali.py -m dab -f <YOURFILENAME> -rs 2048000 -gr

-m choose from  1. dab  2.dvbt  3.gsm
-rs set samplerate default is 2048000
-gr to enable display of graph

### Troubleshoot

ImportError: Error loading librtlsdr
Possible Solution : Add the following .dll/.so files to PATH
                    1. librtlsdr
                    2. libusb-1.0
                    3. rtlsdr



for more details visit [website](https://aerospaceresearch.net/?page_id=2111)