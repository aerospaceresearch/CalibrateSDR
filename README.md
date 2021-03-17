# CalibrateSDR
what is my SDR frequency?


## Troubleshooting

If running the program throws error- ```AttributeError: python: undefined symbol: rtlsdr_get_device_count```, try this:
 
Refer to this [issue](https://github.com/roger-/pyrtlsdr/issues/7#issuecomment-47391543). If it still persists, build [librtlsdr](https://github.com/librtlsdr/librtlsdr) from it source and make sure it's path is defined correctly. 

* Arch-based OS: use AUR source [rtl-sdr-librtlsdr](https://aur.archlinux.org/packages/rtl-sdr-librtlsdr-git/)
* Ubuntu/ Debiam based OS: Run ```sudo apt update && sudo apt install librtlsdr-dev```

Note: After installing, make sure PATH has been define accordingly, for example: ```export LD_LIBRARY_PATH="/usr/local/lib"```
