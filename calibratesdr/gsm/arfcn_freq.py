# This code can be used to get the frequency from AFRCN.
# For more information: http://www.telecomabc.com/a/arfcn.html

def arfcn_selector(arg):
    switcher = {
        "GSM_850": (128, 251),
        "GSM_R_900": (955, 1023),
        "GSM_900": (1, 124),
        "GSM_E_900": (0, 124),
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
        if(band_indicator):
            band_indicator = "GSM_850"
            return 824.2e6 + 0.2e6 * (arfcn - 128) + 45.0e6

    if 1 <= arfcn and arfcn <= 124:
        if(band_indicator != "GSM_E_900"):
            band_indicator = "GSM_900"
        return 890.0e6 + 0.2e6 * arfcn + 45.0e6

    if arfcn == 0:
        if band_indicator:
            band_indicator = "GSM_E_900"
        return 935e6

    if 955 <= arfcn and arfcn <= 1023:
        if band_indicator:
            if 975 <= arfcn:
                band_indicator = "GSM_E_900"
            else:
                band_indicator = "GSM_R_900"
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
        if band_indicator:
            band_indicator = "DCS_1800"
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
        print(f"Scanning all GSM frequencies in {band_indicator}")
        (start, end) = arfcn_selector(band_indicator)
        gsm_freq = []
        for arfcn_no in range(start, end+1):
            gsm_freq.append(arfcn_to_freq(band_indicator, arfcn=arfcn_no))
    return gsm_freq


if __name__ == "__main__":
    print("GSM Bands: \n\t=>GSM_850\n\t=>GSM_R_900\n\t=>GSM_900\n\t=>GSM_E_900\n\t=>DCS_1800\n\t=>PCS_1900")
    gsm_band = input("Enter band you would like to scan:  ")
    gsm_freq = channels(gsm_band)
    print(gsm_freq)


#Pending ARFCN 
# - GSM_R_900 0-124
# - GSM_E_900 975-1023