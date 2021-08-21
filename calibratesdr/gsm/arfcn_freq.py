# This code can be used to get the frequency from AFRCN.
# For more information: http://www.telecomabc.com/a/arfcn.html

from logging import raiseExceptions


def arfcn_selector(arg):
    switcher = {
        "GSM_850": (128, 251),
        "GSM_R_900": (0, 124, 955, 1023),
        "GSM_900": (1, 124),
        "GSM_E_900": (975, 1023, 0, 124),
        "DCS_1800": (512, 885),
        "PCS_1900": (512, 810)
    }
    return switcher.get(arg, -1)


def arfcn_to_freq(band_indicator, arfcn):
    """
    Input: arfcn = absolute radio-frequency channel number (ARFCN)
           band_indicator = band designation 
           (for more info: https://en.wikipedia.org/wiki/Absolute_radio-frequency_channel_number)

    Output: frequency calucalated
            returns -1 for incorrect arfcn
    """

    if 128 <= arfcn and arfcn <= 251:
        if(band_indicator == "GSM_850"):
            return 824.2e6 + 0.2e6 * (arfcn - 128) + 45.0e6

    if 1 <= arfcn and arfcn <= 124:
        if(band_indicator in ("GSM_900", "GSM_E_900", "GSM_R_900")):
            return 890.0e6 + 0.2e6 * arfcn + 45.0e6

    if arfcn == 0:
        if band_indicator in ("GSM_E_900", "GSM_R_900"):
            return 935e6

    if 955 <= arfcn and arfcn <= 1023:
        if band_indicator in ("GSM_E_900", "GSM_R_900"):
            if 975 <= arfcn and arfcn <= 1023 and band_indicator == "GSM_E_900":
                return 890.0e6 + 0.2e6 * (arfcn - 1024) + 45.0e6
            elif band_indicator == "GSM_R_900":
                return 890.0e6 + 0.2e6 * (arfcn - 1024) + 45.0e6

    if 512 <= arfcn and arfcn <= 810:
        if not band_indicator:
            print(f"Error: ambiguous arfcn: {arfcn}")
            return -1
        if band_indicator == "DCS_1800":
            return 1710.2e6 + 0.2e6 * (arfcn - 512) + 95.0e6
        if band_indicator == "PCS_1900":
            return 1850.2e6 + 0.2e6 * (arfcn - 512) + 80.0e6

        print(
            f"Error: bad (arfcn, band indicator) pair: ({arfcn}, {band_indicator}")
        return -1
    if 811 <= arfcn and arfcn <= 885:
        if band_indicator == "DCS_1800":
            return 1710.2e6 + 0.2e6 * (arfcn - 512) + 95.0e6

    print(f"Error: bad arfcn: {arfcn}")
    return -1


def freq_to_arfcn(freq, band_indicator):

    if 869.2e6 <= freq and freq <= 893.8e6:
        if band_indicator:
            band_indicator = "GSM_850"
        return ((freq - 869.2e6)/0.2e6) + 128

    if 921.2e6 <= freq and freq <= 925.0e6:
        if(band_indicator):
            band_indicator = "GSM_R_900"
        return ((freq - 935e6) / 0.2e6) + 1024

    if 935.2e6 <= freq and freq <= 959.8e6:
        if(band_indicator):
            band_indicator = "GSM_900"
        return ((freq - 935e6) / 0.2e6)

    if 935.0e6 == freq:
        if(band_indicator):
            band_indicator = "GSM_E_900"
        return 0

    if 925.2e6 <= freq and freq <= 934.8e6:
        if(band_indicator):
            band_indicator = "GSM_E_900"
        return ((freq - 935e6) / 0.2e6) + 1024

    if 1805.2e6 <= freq and freq <= 1879.8e6:
        if(band_indicator):
            band_indicator = "DCS_1800"
        return ((freq - 1805.2e6) / 0.2e6) + 512

    if 1930.2e6 <= freq and freq <= 1989.8e6:
        if(band_indicator):
            band_indicator = "PCS_1900"
        return ((freq - 1930.2e6) / 0.2e6) + 512

    print(f"error: bad frequency: {freq}")
    return -1


def channels(band_indicator, arfcn=None):

    if arfcn == None:
        print(f"Scanning all GSM frequencies in band: {band_indicator}")
        arfcn_in = arfcn_selector(band_indicator)
        gsm_freq = []
        if len(arfcn_in) == 2:
            (start, end) = arfcn_in
            for arfcn_no in range(start, end+1):
                gsm_freq.append(arfcn_to_freq(band_indicator, arfcn=arfcn_no))
        elif len(arfcn_in) == 4:
            (start0, end0, start1, end1) = arfcn_in
            for arfcn_no in range(start0, end0+1):
                gsm_freq.append(arfcn_to_freq(band_indicator, arfcn=arfcn_no))
            for arfcn_no in range(start1, end1+1):
                gsm_freq.append(arfcn_to_freq(band_indicator, arfcn=arfcn_no))
    else:
        gsm_freq = arfcn_to_freq(band_indicator, arfcn)
        print(
            f"GSM frequency for given {band_indicator} at ARFCN {arfcn}: {gsm_freq}")
    return gsm_freq


def band_key(key):

    if key in ("GSM_850", "850", "GSM-850", "GSM850"):
        band_indicator = "GSM_850"
    elif key in ("GSM_R_900", "R-900", "GSM-R-900", "R-GSM", "Rail"):
        band_indicator = "GSM_R_900"
    elif key in ("GSM_900", "900", "GSM-900", "Primary", "GSM900"):
        band_indicator = "GSM_900"
    elif key in ("GSM_E_900", "E-900", "GSM-E-900", "E-GSM", "Extended"):
        band_indicator = "GSM_E_900"
    elif key in ("DCS_1800", "DCS", "DCS-1800", "1800", "GSM1800"):
        band_indicator = "DCS_1800"
    elif key in ("PCS_1900", "PCS", "PCS-1900", "1900", "GSM1900"):
        band_indicator = "PCS_1900"
    else:
        raise ValueError("Band Not Found")
    return band_indicator


if __name__ == "__main__":
    print("GSM Bands: \n\t=>GSM_850\n\t=>GSM_R_900\n\t=>GSM_900\n\t=>GSM_E_900\n\t=>DCS_1800\n\t=>PCS_1900")
    gsm_band = input("Enter band you would like to scan:  ")
    gsm_band = band_key(gsm_band)
    gsm_freq = channels(gsm_band)
    print(gsm_freq)
