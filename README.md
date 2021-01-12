# CalibrateSDR
## what’s my frequency?

### How to build project?
1. Clone the repository
2. Run cali.py
3. Make sure you have all the required libs (check requirements.txt)

### Basic commands
python.exe cali.py -m dab -f YOURFILENAME -rs 2048000 -gr <br>

<b>-m</b> choose from  dab  / dvbt / gsm <br>
<b>-rs</b> set samplerate default is 2048000  <br>
<b>-gr</b> to enable display of graph <br>

### Troubleshoot

ImportError: Error loading librtlsdr <br>
Possible Solution : Add the following .dll/.so files to PATH
                    <ol>
                    <li>librtlsdr </li>
                    <li>libusb-1.0</li>
                    <li>rtlsdr</li>
                    </ol>


for more details visit [aerospaceresearch.net](https://aerospaceresearch.net/?page_id=2111)