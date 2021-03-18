# CalibrateSDR
what is my SDR frequency?
## Quick Start

__CalibrateSDR__ is a package written in python for determining how precise the oscillator of SDR is due to varition in enviroment.

## Installation Instructions

### Virtual Environment Setup

We can create virtual environment in two ways by using python virtual environment or miniconda. For this guide we will be using **miniconda**, you are free to use any virtual environment setup

**Step 1**: Install miniconda using script and instruction [here](https://docs.conda.io/en/latest/miniconda.html)

**Step 2**: After installation, create a virtualenv with python3.8 as
```
conda create -n env_name python=3.8
```
**Step 3**: Activate your virtualenv
```
conda activate env_name
```
*Rest of the guide will assume that virtualenv is activated.

### Linux Users
Run the following commands to install **CalibrateSDR**:

**Step 1**: Clone the repository
```
git clone https://github.com/aerospaceresearch/CalibrateSDR/
```
**Step 2**: Change directory to CalibrateSDR
```
cd CalibrateSDR
```
**Step 3**: Install required dependencies
```
python setup.py install
```
or manually install with
```
pip install -r requirements.txt
```
**Step 4**: Check your File
```
python cali.py -m [YOUR MODE] -f [YOUR FILE NAME] -rs [YOUR SAMPLE RATE] -gr
```
### Windows Users
<!-- Test for windows -->
<br/>
<br/>
<br/>

## Troubleshooting

If running the program throws error-
```
AttributeError: python: undefined symbol: rtlsdr_get_device_count
```
Try this:
 
Refer to this [issue](https://github.com/roger-/pyrtlsdr/issues/7#issuecomment-47391543). If it still persists, build [librtlsdr](https://github.com/librtlsdr/librtlsdr) from it source and make sure it's path is defined correctly. 
<br/>
* Arch-based OS: &nbsp; use AUR source [rtl-sdr-librtlsdr](https://aur.archlinux.org/packages/rtl-sdr-librtlsdr-git/)
<br/>

* Ubuntu/ Debiam based OS: Run 
  ```
  sudo apt update && sudo apt install librtlsdr-dev
  ```
* On Windows, it gets automatically installed while using 
  ```
  pip install pyrtlsdr
  ```

Note: After installing, make sure PATH has been define accordingly, for example: ```export LD_LIBRARY_PATH="/usr/local/lib"```
