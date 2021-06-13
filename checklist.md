### Currentlt working status: GSM Implementation |========>  | (90%)

### Flowscharts working upon:
<br>
<br>
<br>
<br>
<br>
<br>

### Documentation work starts here:
#### [README.md](./README.md)

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

