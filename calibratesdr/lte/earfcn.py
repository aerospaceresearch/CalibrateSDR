"""
Table used can be found here:
     https://www.cablefree.net/wirelesstechnology/4glte/lte-carrier-frequency-earfcn/
     https://www.sqimway.com/lte_band.php
"""

table_earfcn = {
    1: {
        "band": 1,
        "name": "2100",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 2110,
        "FDL_High": 2170,
        "NDL_Min": 0,
        "NDL_Max": 599
    },
    2: {
        "band": 2,
        "name": "1900 PCS",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 1930,
        "FDL_High": 1990,
        "NDL_Min": 600,
        "NDL_Max": 1199
    },
    3: {
        "band": 3,
        "name": "1800+",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 1805,
        "FDL_High": 1880,
        "NDL_Min": 1200,
        "NDL_Max": 1949
    },
    4: {
        "band": 4,
        "name": "AWS-1",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 2110,
        "FDL_High": 2155,
        "NDL_Min": 1950,
        "NDL_Max": 2399
    },
    5: {
        "band": 5,
        "name": "850",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 869,
        "FDL_High": 894,
        "NDL_Min": 2400,
        "NDL_Max": 2649
    },
    6: {
        "band": 6,
        "name": "UMTS only",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 875,
        "FDL_High": 885,
        "NDL_Min": 2650,
        "NDL_Max": 2749
    },
    7: {
        "band": 7,
        "name": "2600",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 2620,
        "FDL_High": 2690,
        "NDL_Min": 2750,
        "NDL_Max": 3449
    },
    8: {
        "band": 8,
        "name": "900 GSM",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 925,
        "FDL_High": 960,
        "NDL_Min": 3450,
        "NDL_Max": 3799
    },
    9: {
        "band": 9,
        "name": "1800",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 1844.9,
        "FDL_High": 1879.9,
        "NDL_Min": 3800,
        "NDL_Max": 4149
    },
    10: {
        "band": 10,
        "name": "AWS-1+",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 2110,
        "FDL_High": 2170,
        "NDL_Min": 4150,
        "NDL_Max": 4749
    },
    11: {
        "band": 11,
        "name": "1500 Lower1+",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 1475.9,
        "FDL_High": 1495.9,
        "NDL_Min": 4750,
        "NDL_Max": 4949
    },
    12: {
        "band": 12,
        "name": "700 a",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 729,
        "FDL_High": 746,
        "NDL_Min": 5010,
        "NDL_Max": 5179
    },
    13: {
        "band": 13,
        "name": "700 b",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 746,
        "FDL_High": 756,
        "NDL_Min": 5180,
        "NDL_Max": 5279
    },
    14: {
        "band": 14,
        "name": "700 PS",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 758,
        "FDL_High": 768,
        "NDL_Min": 5280,
        "NDL_Max": 5379
    },
    17: {
        "band": 17,
        "name": "700 b",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 734,
        "FDL_High": 746,
        "NDL_Min": 5730,
        "NDL_Max": 5849
    },
    18: {
        "band": 18,
        "name": "800 Lower",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 860,
        "FDL_High": 875,
        "NDL_Min": 5850,
        "NDL_Max": 5999
    },
    19: {
        "band": 19,
        "name": "800 Upper",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 875,
        "FDL_High": 890,
        "NDL_Min": 6000,
        "NDL_Max": 6149
    },
    20: {
        "band": 20,
        "name": "800 DD",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 791,
        "FDL_High": 821,
        "NDL_Min": 6150,
        "NDL_Max": 6449
    },
    21: {
        "band": 21,
        "name": "1500 Upper",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 1495.9,
        "FDL_High": 1510.9,
        "NDL_Min": 6450,
        "NDL_Max": 6599
    },
    22: {
        "band": 22,
        "name": "3500",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 3510,
        "FDL_High": 3590,
        "NDL_Min": 6600,
        "NDL_Max": 7399
    },
    23: {
        "band": 23,
        "name": "2000 S-band",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 2180,
        "FDL_High": 2200,
        "NDL_Min": 7500,
        "NDL_Max": 7699
    },
    24: {
        "band": 24,
        "name": "1600 L-band",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 1525,
        "FDL_High": 1559,
        "NDL_Min": 7700,
        "NDL_Max": 8039
    },
    25: {
        "band": 25,
        "name": "1900+",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 1930,
        "FDL_High": 1995,
        "NDL_Min": 8040,
        "NDL_Max": 8689
    },
    26: {
        "band": 26,
        "name": "850+",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 859,
        "FDL_High": 894,
        "NDL_Min": 8690,
        "NDL_Max": 9039
    },
    27: {
        "band": 27,
        "name": "800 SMR",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 852,
        "FDL_High": 869,
        "NDL_Min": 9040,
        "NDL_Max": 9209
    },
    28: {
        "band": 28,
        "name": "700 APT",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 758,
        "FDL_High": 803,
        "NDL_Min": 9210,
        "NDL_Max": 9659
    },
    29: {
        "band": 29,
        "name": "700 d",
        "bandType": "FDD",
        "DLOnly": True,
        "FDL_Low": 717,
        "FDL_High": 728,
        "NDL_Min": 9660,
        "NDL_Max": 9769
    },
    30: {
        "band": 30,
        "name": "2300 WCS",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 2350,
        "FDL_High": 2360,
        "NDL_Min": 9770,
        "NDL_Max": 9869
    },
    31: {
        "band": 31,
        "name": "450",
        "bandType": "FDD",
        "DLOnly": False,
        "FDL_Low": 462.5,
        "FDL_High": 467.5,
        "NDL_Min": 9870,
        "NDL_Max": 9919
    },
    32: {
        "band": 32,
        "name": "1500 L-band",
        "bandType": "FDD",
        "DLOnly": True,
        "FDL_Low": 1452,
        "FDL_High": 1496,
        "NDL_Min": 9920,
        "NDL_Max": 10359
    },
    33: {
        "band": 33,
        "name": "TD 1900",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1900,
        "FDL_High": 1920,
        "NDL_Min": 36000,
        "NDL_Max": 36199
    },
    34: {
        "band": 34,
        "name": "TD 2000",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 2010,
        "FDL_High": 2025,
        "NDL_Min": 36200,
        "NDL_Max": 36349
    },
    35: {
        "band": 35,
        "name": "TD PCS Lower",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1850,
        "FDL_High": 1910,
        "NDL_Min": 36350,
        "NDL_Max": 36949
    },
    36: {
        "band": 36,
        "name": "TD PCS Upper",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1930,
        "FDL_High": 1990,
        "NDL_Min": 36950,
        "NDL_Max": 37549
    },
    37: {
        "band": 37,
        "name": "TD PCS Center gap",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1910,
        "FDL_High": 1930,
        "NDL_Min": 37550,
        "NDL_Max": 37749
    },
    38: {
        "band": 38,
        "name": "TD 2600",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 2570,
        "FDL_High": 2620,
        "NDL_Min": 37750,
        "NDL_Max": 38249
    },
    39: {
        "band": 39,
        "name": "TD 1900+",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1880,
        "FDL_High": 1920,
        "NDL_Min": 38250,
        "NDL_Max": 38649
    },
    40: {
        "band": 40,
        "name": "TD 2300",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 2300,
        "FDL_High": 2400,
        "NDL_Min": 38650,
        "NDL_Max": 39649
    },
    41: {
        "band": 41,
        "name": "TD 2500",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 2496,
        "FDL_High": 2690,
        "NDL_Min": 39650,
        "NDL_Max": 41589
    },
    42: {
        "band": 42,
        "name": "TD 3500",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 3400,
        "FDL_High": 3600,
        "NDL_Min": 41590,
        "NDL_Max": 43589
    },
    43: {
        "band": 43,
        "name": "TD 3700",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 3600,
        "FDL_High": 3800,
        "NDL_Min": 43590,
        "NDL_Max": 45589
    },
    44: {
        "band": 44,
        "name": "TD 700",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 703,
        "FDL_High": 803,
        "NDL_Min": 45590,
        "NDL_Max": 46589
    },
    45: {
        "band": 45,
        "name": "TD 1500",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1447,
        "FDL_High": 1467,
        "NDL_Min": 46590,
        "NDL_Max": 46789
    },
    46: {
        "band": 46,
        "name": "TD Unlicensed",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 5150,
        "FDL_High": 5925,
        "NDL_Min": 46790,
        "NDL_Max": 54539
    },
    47: {
        "band": 47,
        "name": "TD V2X",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 5855,
        "FDL_High": 5925,
        "NDL_Min": 54540,
        "NDL_Max": 55239
    },
    48: {
        "band": 48,
        "name": "TD 3600",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 3550,
        "FDL_High": 3700,
        "NDL_Min": 55240,
        "NDL_Max": 56739
    },
    49: {
        "band": 49,
        "name": "TD 3600r",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 3550,
        "FDL_High": 3700,
        "NDL_Min": 56740,
        "NDL_Max": 58239
    },
    50: {
        "band": 50,
        "name": "TD 1500+",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1432,
        "FDL_High": 1517,
        "NDL_Min": 58240,
        "NDL_Max": 59089
    },
    51: {
        "band": 51,
        "name": "TD 1500-",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 1427,
        "FDL_High": 1432,
        "NDL_Min": 59090,
        "NDL_Max": 59139
    },
    52: {
        "band": 52,
        "name": "TD 3300",
        "bandType": "TDD",
        "DLOnly": True,
        "FDL_Low": 3300,
        "FDL_High": 3400,
        "NDL_Min": 59140,
        "NDL_Max": 60139
    }
}


def earfcn_to_freq(band, dl_earfcn=None):

    NDL_Offset = table_earfcn[band]['NDL_Min']
    FDL_Low = table_earfcn[band]['FDL_Low']

    if dl_earfcn is not None:
        downlink_freq = FDL_Low + 0.1 * (dl_earfcn-NDL_Offset)

    return (downlink_freq)


if __name__ == "__main__":
    print("Started mode LTE (4G)", end="\n")
    band = int(input("Band Index: "))
    dl_earfcn = int(input("Downlink E-ARFCN: "))
    downlink_freq = earfcn_to_freq(band, dl_earfcn)
    print(f"Downlink: {downlink_freq} MHz")
