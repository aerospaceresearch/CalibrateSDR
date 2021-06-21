# CalibrateSDR
_A precise tool to calculate offset of SDR device_ 📻

__CalibrateSDR__ is designed to accurately determine the frequency offset of an SDR via an IQ recording sample.

Cheaper SDRs use a low-quality crystal oscillator which usually has a large offset from the ideal frequency. Furthermore, that frequency offset will change as the dongle warms up or as the ambient temperature changes. The end result is that any signals received will not be at the correct frequency, and they would drift as the temperature changes. 

CalibrateSDR can be used with almost any SDR to determine the frequency offset. Signal standards like GSM, LTE, NOAA-Weather Satellites, DVB-T (use their sync pulses within the data) can be used. Currently, it uses the pyrtlsdr package, which makes it work with RTL-SDR.
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>




## Troubleshooting

If running the program throws error- ```AttributeError: python: undefined symbol: rtlsdr_get_device_count```, try this:
 
Refer to this [issue](https://github.com/roger-/pyrtlsdr/issues/7#issuecomment-47391543). If it still persists, build [librtlsdr](https://github.com/librtlsdr/librtlsdr) from it source and make sure it's path is defined correctly. 

* Arch-based OS: use AUR source [rtl-sdr-librtlsdr](https://aur.archlinux.org/packages/rtl-sdr-librtlsdr-git/)
* Ubuntu/ Debiam based OS: Run ```sudo apt update && sudo apt install librtlsdr-dev```
* On Windows, it gets automatically installed while using ```pip install pyrtlsdr```

Note: After installing, make sure PATH has been define accordingly, for example: ```export LD_LIBRARY_PATH="/usr/local/lib"```
