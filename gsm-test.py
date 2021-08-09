import argparse
import os
from tqdm import tqdm
import time
import calibratesdr as cali


def get_gsm(input, sdr=True):
    
    from rtlsdr import RtlSdr
    filename = "tmp.dat"
    device = input["rd"]
    sdr = RtlSdr(device_index=device)
    rs = input["rs"]
    rg = input["rg"]
    ns = rs * input["nsec"]  # seconds
    c = input["c"]

 