# CalibrateSDR
## what’s my frequency?

### How to build project?
1. Clone the repository
2. Run cali.py
3. Make sure you have all the required libs (check requirements.txt)

### Basic commands
python.exe cali.py -m dab -f YOURFILENAME -rs 2048000 -gr <br>

-m choose from  1. dab  2.dvbt  3.gsm <br>
-rs set samplerate default is 2048000  <br>
-gr to enable display of graph <br>

### Troubleshoot

ImportError: Error loading librtlsdr
Possible Solution : Add the following .dll/.so files to PATH
                    <ol>
                    <li>librtlsdr </li>
                    <li>libusb-1.0</li>
                    <li>rtlsdr</li>
                    </ol>


for more details visit [https://aerospaceresearch.net](https://aerospaceresearch.net/?page_id=2111)